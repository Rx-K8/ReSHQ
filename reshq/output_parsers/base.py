from abc import ABC, abstractmethod


class BaseOutputParser(ABC):
    @abstractmethod
    def parse(self, text) -> list[str]:
        raise NotImplementedError
