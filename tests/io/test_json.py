import json
from unittest.mock import mock_open, patch

import pytest

from reshq.io.json import JsonReadHandler, JsonWriteHandler


@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "json_test" / "test.json"


class TestJsonFileHandler:
    def test_write_creates_file(self, temp_file):
        handler = JsonWriteHandler(temp_file)
        data = {"key": "value"}

        handler.write(data)

        assert temp_file.exists()

    def test_write_correct_content(self, temp_file):
        handler = JsonWriteHandler(temp_file)
        data = {"key": "value"}

        handler.write(data)

        with open(temp_file, "r", encoding="utf-8") as file:
            content = json.load(file)

        assert content == data

    def test_write_creates_directory(self, tmp_path):
        nested_dir = tmp_path / "nested_dir"
        file_path = nested_dir / "test.json"
        handler = JsonWriteHandler(file_path)
        data = {"key": "value"}

        handler.write(data)

        assert file_path.exists()
        assert nested_dir.exists()

    def test_validation_extension(self, tmp_path):
        file_path = tmp_path / "test" / "test.txt"
        with pytest.raises(ValueError, match="File extension must be .json"):
            JsonWriteHandler(file_path)


class TestJsonReadHandler:
    def test_read_success(self, tmp_path):
        file_path = tmp_path / "test.json"
        handler = JsonReadHandler(file_path)
        mock_data = {"key": "value"}
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(mock_data))
        ):
            result = handler.read()
            assert result == mock_data

    def test_read_file_not_found(self, tmp_path):
        self.file_path = tmp_path / "test.json"
        self.handler = JsonReadHandler(self.file_path)
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                self.handler.read()

    def test_read_non_existent_file(self, tmp_path):
        file_path = tmp_path / "non_existent_file.json"
        handler = JsonReadHandler(file_path)

        assert not file_path.exists()

        with pytest.raises(FileNotFoundError):
            handler.read()

    def test_read_json_decode_error(self, tmp_path):
        self.file_path = tmp_path / "test.json"
        self.handler = JsonReadHandler(self.file_path)
        with patch("builtins.open", mock_open(read_data="not a json")):
            with pytest.raises(json.JSONDecodeError):
                self.handler.read()

    def test_read_io_error(self, tmp_path):
        self.file_path = tmp_path / "test.json"
        self.handler = JsonReadHandler(self.file_path)
        with patch("builtins.open", side_effect=IOError):
            with pytest.raises(IOError):
                self.handler.read()
