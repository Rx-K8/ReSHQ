import json

import pytest

from reshq.io.json import JsonFileHandler


@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "json_test" / "test.json"


class TestJsonFileHandler:
    def test_write_creates_file(self, temp_file):
        handler = JsonFileHandler(temp_file)
        data = {"key": "value"}

        handler.write(data)

        assert temp_file.exists()

    def test_write_correct_content(self, temp_file):
        handler = JsonFileHandler(temp_file)
        data = {"key": "value"}

        handler.write(data)

        with open(temp_file, "r", encoding="utf-8") as file:
            content = json.load(file)

        assert content == data

    def test_write_creates_directory(self, tmp_path):
        nested_dir = tmp_path / "nested_dir"
        file_path = nested_dir / "test.json"
        handler = JsonFileHandler(file_path)
        data = {"key": "value"}

        handler.write(data)

        assert file_path.exists()
        assert nested_dir.exists()

    def test_validation_extension(self, tmp_path):
        file_path = tmp_path / "test" / "test.txt"
        with pytest.raises(ValueError, match=f"File extension must be .json"):
            JsonFileHandler(file_path)
