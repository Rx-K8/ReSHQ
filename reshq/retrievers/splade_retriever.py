from types import MappingProxyType

from pyserini.search.lucene import LuceneImpactSearcher, LuceneSearcher

from reshq.output_formats.search_result import SearchResults
from reshq.result_converters.factory import converter_factory
from reshq.retrievers.abc import Retriever
from reshq.retrievers.bm25_retriever import bm25flat_index_mappings

splade_index_mappings = MappingProxyType(
    {
        # BEIR
        "beir_climate_fever": "beir-v1.0.0-climate-fever.splade-pp-ed",
        # TREC
        "trec2019": "msmarco-v1-passage.splade-pp-ed",
        "trec2020": "msmarco-v1-passage.splade-pp-ed",
    }
)


class Splade(Retriever):
    def __init__(self, benchmark: str) -> None:
        self.name: str = "splade"
        self.benchmark = benchmark
        self.passage_type = splade_index_mappings[self.benchmark]
        self.retriever = LuceneImpactSearcher.from_prebuilt_index(
            self.passage_type,
            "naver/splade-cocondenser-ensembledistil",
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
