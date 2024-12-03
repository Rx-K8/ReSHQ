from reshq.result_converters.BEIRConverter import BEIRConverter
from reshq.result_converters.TRECConverter import TRECConverter

converter_mappings = {
    "trec2019": "trec",
    "trec2020": "trec",
    "beir_climate_fever": "beir",
}


def converter_factory(benchmark: str):
    if converter_mappings[benchmark] == "trec":
        return TRECConverter()
    elif converter_mappings[benchmark] == "beir":
        return BEIRConverter()
    else:
        raise ValueError(f"Unknown benchmark: {benchmark}")
