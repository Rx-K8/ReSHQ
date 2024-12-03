import sys

from pyserini.search import get_qrels, get_topics
from tqdm import tqdm

from reshq.cachers.query_cacher import QueryCacher
from reshq.io.text import TextWriteHandler
from reshq.output_parsers.list import NumberedListOutputParser
from reshq.paths import VALOUTPUT_DIR
from reshq.retrievers.bm25_retriever import BM25
from reshq.retrievers.reshq_retriever import ReSHQ
from reshq.retrievers.splade_retriever import Splade
from reshq.topics import TOPICS


def reshq_trec2019_initialsearch_by_bm25():
    bench_mark = "trec2019"
    initial_search = BM25(bench_mark)
    top_k = 100
    model_id = "unsloth/llama-3-8b-Instruct-bnb-4bit"
    output_parser = NumberedListOutputParser()
    query_cacher = QueryCacher(initial_search.passage_type)
    reshq = ReSHQ(query_cacher, initial_search, model_id, output_parser)

    topics = get_topics(TOPICS[bench_mark])
    qrels = get_qrels(TOPICS[bench_mark])
    results = []
    for qid in tqdm(topics):
        if qid in qrels:
            query = topics[qid]["title"]
            hits = reshq.retrieve(query, top_k)
            validation_outputs = hits.to_validation(qid)
            results.extend(validation_outputs)

    output_file = (
        VALOUTPUT_DIR
        / f"{reshq.name}_{bench_mark}_{initial_search.name}_{top_k}.txt"
    )
    TextWriteHandler(output_file).write(results)


def reshq_trec2019_initialsearch_by_splade():
    bench_mark = "trec2019"
    initial_search = Splade(bench_mark)
    top_k = 10
    model_id = "unsloth/llama-3-8b-Instruct-bnb-4bit"
    output_parser = NumberedListOutputParser()
    query_cacher = QueryCacher(initial_search.passage_type)
    reshq = ReSHQ(query_cacher, initial_search, model_id, output_parser)

    topics = get_topics(TOPICS[bench_mark])
    qrels = get_qrels(TOPICS[bench_mark])
    results = []
    for qid in tqdm(topics):
        if qid in qrels:
            query = topics[qid]["title"]
            hits = reshq.retrieve(query, top_k)
            validation_outputs = hits.to_validation(qid)
            results.extend(validation_outputs)

    output_file = (
        VALOUTPUT_DIR
        / f"{reshq.name}_{bench_mark}_{initial_search.name}_{top_k}.txt"
    )
    TextWriteHandler(output_file).write(results)


def reshq_climatefever_initialsearch_by_splade():
    bench_mark = "beir_climate_fever"
    # initial_search = Splade(bench_mark)
    initial_search = BM25(bench_mark)
    top_k = 100
    # model_id = "unsloth/llama-3-8b-Instruct-bnb-4bit"
    # output_parser = NumberedListOutputParser()
    # query_cacher = QueryCacher(initial_search.passage_type)
    # reshq = ReSHQ(query_cacher, initial_search, model_id, output_parser)

    topics = get_topics(TOPICS[bench_mark])
    qrels = get_qrels(TOPICS[bench_mark])
    results = []
    for qid in tqdm(topics):
        if qid in qrels:
            query = topics[qid]["title"]
            # hits = reshq.retrieve(query, top_k)
            hits = initial_search.retrieve(query, top_k)
            validation_outputs = hits.to_validation(qid)
            results.extend(validation_outputs)

    output_file = (
        VALOUTPUT_DIR
        # / f"{reshq.name}_{bench_mark}_{initial_search.name}_{top_k}.txt"
        / f"{initial_search.name}_{bench_mark}_{initial_search.name}_{top_k}.txt"
    )
    TextWriteHandler(output_file).write(results)


def main():
    # reshq_trec2019_initialsearch_by_bm25()
    # reshq_trec2019_initialsearch_by_splade()
    reshq_climatefever_initialsearch_by_splade()

    return 0


if __name__ == "__main__":
    sys.exit(main())
