import argparse
import sys

from pyserini.search import get_qrels, get_topics
from tqdm import tqdm

from reshq.cachers.query_cacher import QueryCacher
from reshq.io.text import TextWriteHandler
from reshq.output_parsers.list import NumberedListOutputParser
from reshq.paths import VALOUTPUT_DIR
from reshq.retrievers.bm25_retriever import BM25
from reshq.retrievers.contriever_retriever import Contriever
from reshq.retrievers.reshq_retriever import ReSHQ
from reshq.retrievers.splade_retriever import Splade
from reshq.topics import TOPICS


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--bench_mark", type=str, required=True)
    parser.add_argument("--initial_search", type=str, required=True)

    args = parser.parse_args()
    return args


def get_initial_search(initial_search_name, bench_mark):
    if initial_search_name == "BM25":
        return BM25(bench_mark)
    elif initial_search_name == "Contriever":
        return Contriever(bench_mark)
    else:
        raise ValueError


def run(bench_mark, model_id, initial_search_name):
    initial_search = get_initial_search(initial_search_name, bench_mark)
    top_k = 100
    output_parser = NumberedListOutputParser()
    query_cacher = QueryCacher(bench_mark)
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


def main():
    args = args_parser()
    bench_mark = args.bench_mark
    model_id = args.model
    initial_search_name = args.initial_search
    run(bench_mark, model_id, initial_search_name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
