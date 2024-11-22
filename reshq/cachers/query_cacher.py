from reshq.io.json import JsonReadHandler, JsonWriteHandler
from reshq.paths import CREATED_QUERY_CACHE_FILE


class QueryCacher:
    def __init__(self, cache_filepath=CREATED_QUERY_CACHE_FILE):
        self.cache_filepath = cache_filepath
        self._docid_queries_mappings: dict[str, list[str]] = self._load_cache()
        self.write_handler = JsonWriteHandler(self.cache_filepath)

    def _load_cache(self):
        if self.cache_filepath.exists():
            return JsonReadHandler(self.cache_filepath).read()
        return {}

    def cache_exists(self, doc_id):
        return doc_id in self._docid_queries_mappings

    def add_queries(self, doc_id, queries):
        self._docid_queries_mappings[doc_id] = queries

    def get_queries(self, doc_id):
        return self._docid_queries_mappings.get(doc_id)

    def write(self):
        self.write_handler.write(self._docid_queries_mappings)
