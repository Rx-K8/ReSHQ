from reshq.result_converters.TRECConverter import TRECConverter

converter_mappings = {"trec2019": "trec", "trec2020": "trec"}


def converter_factory(benchmark: str):
    if converter_mappings[benchmark] == "trec":
        return TRECConverter()
    else:
        raise ValueError(f"Unknown benchmark: {benchmark}")
