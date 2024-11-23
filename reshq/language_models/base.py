from abc import ABC, abstractmethod


class BaseLanguageModel(ABC):
    @abstractmethod
    def generate(self, texts: list[str]) -> list[str]:
        raise NotImplementedError
