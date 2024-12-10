from reshq.io.json import JsonReadHandler, JsonWriteHandler
from reshq.paths import CREATED_QUERY_CACHE_DIR
from reshq.logger_config import logger


class QueryCacher:
    def __init__(self, bentch_mark, cache_dirpath=CREATED_QUERY_CACHE_DIR):
        self.cache_filepath = (
            cache_dirpath / f"created_query_cache_{bentch_mark}.json"
        )
        self._docid_queries_mappings: dict[str, list[str]] = self._load_cache()
        self.write_handler = JsonWriteHandler(self.cache_filepath)

    def _load_cache(self):
        if self.cache_filepath.exists():
            logger.info(f"Loading cache from {self.cache_filepath}")
            return JsonReadHandler(self.cache_filepath).read()
        return {}

    def cache_exists(self, doc_id):
        return doc_id in self._docid_queries_mappings

    def add_queries(self, doc_id, queries):
        self._docid_queries_mappings[doc_id] = queries
        self.write()

    def get_queries(self, doc_id):
        return self._docid_queries_mappings.get(doc_id)

    def write(self):
        self.write_handler.write(self._docid_queries_mappings)
