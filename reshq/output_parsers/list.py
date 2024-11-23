import re

from base import BaseOutputParser


class NumberedListOutputParser(BaseOutputParser):
    def __init__(self):
        self.pattern: str = r"\d+\.\s([^\n]+)"

    def parse(self, text: str) -> list[str]:
        return re.findall(self.pattern, text)
