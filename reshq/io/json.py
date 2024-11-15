import json
from pathlib import Path

from reshq.io.abc import WriteFileHandler
from reshq.io.utils import make_directory
from reshq.logger_config import logger


class JsonFileHandler(WriteFileHandler):
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
