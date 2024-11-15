from abc import ABC, abstractmethod


class WriteFileHandler(ABC):
    def __init__(self, file_path, extension):
        self.extension = extension
        self.file_path = file_path
        self._validation_extension()

    @abstractmethod
    def write(self, data):
        raise NotImplementedError

    def _validation_extension(self):
        if self.file_path.suffix != self.extension:
            raise ValueError(f"File extension must be {self.extension}")
