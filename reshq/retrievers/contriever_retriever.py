from types import MappingProxyType

from pyserini.encode import AutoQueryEncoder
from pyserini.search import get_qrels, get_topics
from pyserini.search.faiss import FaissSearcher
from pyserini.search.lucene import LuceneSearcher
from tqdm import tqdm

from reshq.io.text import TextWriteHandler
from reshq.output_formats.search_result import SearchResults
from reshq.paths import VALOUTPUT_DIR
from reshq.result_converters.factory import converter_factory
from reshq.retrievers.abc import Retriever
from reshq.retrievers.bm25_retriever import bm25flat_index_mappings
from reshq.topics import TOPICS

contriever_index_mappings = MappingProxyType(
    {
        # BEIR
        "beir_climate_fever": "beir-v1.0.0-climate-fever.contriever",
    }
)


class Contriever(Retriever):
    def __init__(self, benchmark: str) -> None:
        self.name: str = "convetrter"
        self.benchmark = benchmark
        self.passage_type = contriever_index_mappings[benchmark]
        self.encoder = AutoQueryEncoder(
            encoder_dir="facebook/contriever", pooling="mean"
        )
        self.retriever = FaissSearcher.from_prebuilt_index(
            self.passage_type,
            self.encoder,
        )
        self.corpus = LuceneSearcher.from_prebuilt_index(
            bm25flat_index_mappings[self.benchmark]
        )
        self.converter = converter_factory(benchmark)

    def retrieve(self, query: str, top_k: int) -> SearchResults:
        hits = self.retriever.search(query, top_k)
        search_results = SearchResults()
        for hit in hits:
            doc_id = hit.docid
            content = self.converter.convert(self.corpus.doc(doc_id).raw())
            score = hit.score
            search_results.add_search_result(query, doc_id, content, score)
        return search_results


def main():
    bench_mark = "beir_climate_fever"
    initial_search = Contriever(bench_mark)
    top_k = 100

    topics = get_topics(TOPICS[bench_mark])
    qrels = get_qrels(TOPICS[bench_mark])
    results = []
    for qid in tqdm(topics):
        if qid in qrels:
            query = topics[qid]["title"]
            hits = initial_search.retrieve(query, top_k)
            validation_outputs = hits.to_validation(qid)
            results.extend(validation_outputs)

    output_file = (
        VALOUTPUT_DIR
        / f"{initial_search.name}_{bench_mark}_{initial_search.name}_{top_k}.txt"
    )
    TextWriteHandler(output_file).write(results)


if __name__ == "__main__":
    main()
