import textwrap
from typing import Optional

from reshq.encoders.contriever import ContrieverEncoder
from reshq.language_models.lm import LanguageModel
from reshq.logger_config import logger
from reshq.output_formats.search_result import SearchResults
from reshq.output_parsers.base import BaseOutputParser
from reshq.output_parsers.list import NumberedListOutputParser
from reshq.retrievers.abc import Retriever
from reshq.retrievers.bm25_retriever import BM25

TEMPLATE = textwrap.dedent(
    """\
    Please come up with questions that can be answered by the document.
    Please output as a numbered list.
    Only respond with the queries, nothing else.

    ### Document:
    {}

    ### {} queries:
    """
)


class ReSHQ(Retriever):
    def __init__(
        self,
        query_cacher,
        initial_retriever: Retriever,
        model_id: str,
        output_parser: Optional[BaseOutputParser] = None,
    ):
        self.name: str = "reshq"
        self.init_retriever = initial_retriever
        self.generator = LanguageModel(model_id, output_parser)
        self.query_cacher = query_cacher
        self.contriever = ContrieverEncoder()
        self.created_queries_num = 5

    def retrieve(self, query: str, top_k: int):
        initial_hits = self.init_retriever.retrieve(query, top_k)
        self._generate_queries(initial_hits)

        research_results = SearchResults()
        for hit in initial_hits:
            doc_id = hit.doc_id
            created_queries = self.query_cacher.get_queries(doc_id)
            scores = [
                self.contriever.dot_score(query, created_query)
                for created_query in created_queries
            ]
            max_score = max(scores)
            research_results.add_search_result(
                query, doc_id, hit.content, max_score
            )
        research_results.sort()
        return research_results

    def _generate_queries(self, hits: SearchResults):
        while True:
            doc_ids = []
            prompts = []

            for hit in hits:
                doc_id = hit.doc_id
                if not self.query_cacher.cache_exists(doc_id):
                    doc_ids.append(doc_id)
                    content = hit.content
                    prompt = self._create_prompt(content)
                    prompts.append(prompt)
            if not doc_ids:
                break

            outputs = self.generator.generate(prompts)
            for doc_id, output in zip(doc_ids, outputs):
                logger.info(doc_id)
                try:
                    self.query_cacher.add_queries(
                        doc_id, self._validate_queries(output)
                    )
                except ValueError as e:
                    logger.error(doc_id)
                    logger.error(output)

    def _validate_queries(self, output: list[str]):
        if len(output) >= self.created_queries_num:
            return output[: self.created_queries_num]
        raise ValueError(
            f"Output must have at least {self.created_queries_num} queries"
        )

    def _create_prompt(self, text: str) -> str:
        return TEMPLATE.format(text, self.created_queries_num)


if __name__ == "__main__":
    retriever = BM25("trec2019")
    output_parser = NumberedListOutputParser()
    reshq = ReSHQ(
        retriever, "unsloth/llama-3-8b-Instruct-bnb-4bit", output_parser
    )
    hits = reshq.retrieve("What is the capital of Japan", 5)
    print(hits)
