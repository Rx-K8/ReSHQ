from reshq.result_converters.BEIRConverter import BEIRConverter
from reshq.result_converters.TRECConverter import TRECConverter

converter_mappings = {
    # BEIR
    "beir_trec_covid": "beir",
    "beir_bioasq": "beir",
    "beir_nfcorpus": "beir",
    "beir_nq": "beir",
    "beir_hotpotqa": "beir",
    "beir_fiqa": "beir",
    "beir_signal1m": "beir",
    "beir_trec_news": "beir",
    "beir_robust04": "beir",
    "beir_arguana": "beir",
    "beir_webis_touche2020": "beir",
    "beir_quora": "beir",
    "beir_dbpedia_entity": "beir",
    "beir_scidocs": "beir",
    "beir_fever": "beir",
    "beir_climate_fever": "beir",
    "beir_scifact": "beir",
    # TREC
    "trec2019": "trec",
    "trec2020": "trec",
}


def converter_factory(benchmark: str):
    if converter_mappings[benchmark] == "trec":
        return TRECConverter()
    elif converter_mappings[benchmark] == "beir":
        return BEIRConverter()
    else:
        raise ValueError(f"Unknown benchmark: {benchmark}")
