import sys

from pyserini.search import get_qrels, get_topics
from tqdm import tqdm

from reshq.io.text import TextWriteHandler
from reshq.output_parsers.list import NumberedListOutputParser
from reshq.paths import VALOUTPUT_DIR
from reshq.retrievers.bm25_retriever import BM25
from reshq.retrievers.reshq_retriever import ReSHQ
from reshq.topics import TOPICS


def main():
    bench_mark = "trec2019"
    top_k = 100
    model_id = "unsloth/llama-3-8b-Instruct-bnb-4bit"
    initial_search = BM25(bench_mark)
    output_parser = NumberedListOutputParser()
    reshq = ReSHQ(
        initial_search.passage_type, initial_search, model_id, output_parser
    )

    topics = get_topics(TOPICS[bench_mark])
    qrels = get_qrels(TOPICS[bench_mark])

    results = []
    for qid in tqdm(topics):
        if qid in qrels:
            query = topics[qid]["title"]
            hits = reshq.retrieve(query, top_k)
            validation_outputs = hits.to_validation(qid)
            results.extend(validation_outputs)

    output_file = VALOUTPUT_DIR / f"{bench_mark}_{reshq.name}_{top_k}.txt"
    TextWriteHandler(output_file).write(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
