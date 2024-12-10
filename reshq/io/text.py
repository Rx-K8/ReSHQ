from pathlib import Path

from reshq.logger_config import logger

from reshq.io.abc import FileWriteHandler
from reshq.io.utils import make_directory


class TextWriteHandler(FileWriteHandler):
    def __init__(self, file_path: Path, indent: int = 4):
        super().__init__(file_path, ".txt")
        self.indent = indent

    def write(self, data: list[str]) -> None:
        make_directory(self.file_path.parent)
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(data))
        except IOError as e:
            logger.error(f"An error occurred while writing to the file: {e}")
            raise
