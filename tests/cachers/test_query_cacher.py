import json
from pathlib import Path

import pytest

from reshq.cachers.query_cacher import QueryCacher


class TestQueryCacher:
    @pytest.fixture()
    def prepared_file(self, tmp_path):
        self.sample_data = {"name": "John Doe", "age": 30, "city": "New York"}
        tmp_file = tmp_path / "test.json"
        tmp_file.write_text(json.dumps(self.sample_data, indent=4))
        return tmp_file

    def test_load_cache_when_file_exists(self, prepared_file):
        query_cacher = QueryCacher(cache_filepath=prepared_file)
        assert query_cacher._docid_queries_mappings == self.sample_data

    def test_load_cache_when_file_does_not_exists(self, tmp_path):
        not_exist_file = tmp_path / "not_exist.json"
        query_cacher = QueryCacher(not_exist_file)
        assert query_cacher._docid_queries_mappings == {}

    def test_cache_exists(self):
        query_cacher = QueryCacher()
        query_cacher._docid_queries_mappings = {"doc1": ["query1", "query2"]}
        assert query_cacher.cache_exists("doc1") is True
        assert query_cacher.cache_exists("doc2") is False

    def test_add_queries(self):
        query_cacher = QueryCacher()
        query_cacher.add_queries("doc1", ["query1"])
        assert query_cacher._docid_queries_mappings == {"doc1": ["query1"]}

    def test_get_queries(self):
        query_cacher = QueryCacher()
        query_cacher._docid_queries_mappings = {"doc1": ["query1", "query2"]}
        assert query_cacher.get_queries("doc1") == ["query1", "query2"]

    def test_write_cache(self, tmp_path):
        cache_filepath = tmp_path / "test.json"
        query_cacher = QueryCacher(cache_filepath=cache_filepath)
        query_cacher._docid_queries_mappings = {"doc1": ["query1", "query2"]}
        query_cacher.write()

        assert cache_filepath.exists()
        with open(cache_filepath) as f:
            assert json.loads(f.read()) == {"doc1": ["query1", "query2"]}
