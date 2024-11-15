import json
from pathlib import Path

from reshq.io.abc import FileReadHandler, FileWriteHandler
from reshq.io.utils import make_directory
from reshq.logger_config import logger


class JsonWriteHandler(FileWriteHandler):
    def __init__(self, file_path: Path, indent: int = 4):
        super().__init__(file_path, ".json")
        self.indent = indent

    def write(self, data) -> None:
        make_directory(self.file_path.parent)
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=self.indent)
        except IOError as e:
            logger.error(f"An error occurred while writing to the file: {e}")
            raise


class JsonReadHandler(FileReadHandler):
    def __init__(self, file_path):
        super().__init__(file_path, ".json")

    def read(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error("The file does not exist.")
            raise
        except json.JSONDecodeError as e:
            logger.error(
                f"An error occurred while decoding the JSON file: {e}"
            )
            raise
        except IOError as e:
            logger.error(f"An error occurred while reading the file: {e}")
            raise
