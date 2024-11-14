import json

from reshq.result_converters.abc import Converter


class TRECConverter(Converter):
    def convert(self, data: str) -> str:
        dict_doc = json.loads(data)
        return dict_doc["contents"]
