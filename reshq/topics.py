from os.path import join
from types import MappingProxyType

TOPICS = MappingProxyType(
    {
        # BEIR(Benchmarking IR)
        "beir_trec_covid": "beir-v1.0.0-trec-covid",
        "beir_bioasq": "beir-v1.0.0-bioasq",
        "beir_nfcorpus": "beir-v1.0.0-nfcorpus",
        "beir_nq": "beir-v1.0.0-nq",
        "beir_hotpotqa": "beir-v1.0.0-hotpotqa",
        "beir_fiqa": "beir-v1.0.0-fiqa",
        "beir_signal1m": "beir-v1.0.0-signal1m",
        "beir_trec_news": "beir-v1.0.0-trec-news",
        "beir_robust04": "beir-v1.0.0-robust04",
        "beir_arguana": "beir-v1.0.0-arguana",
        "beir_webis_touche2020": "beir-v1.0.0-webis-touche2020",
        "beir_quora": "beir-v1.0.0-quora",
        "beir_dbpedia_entity": "beir-v1.0.0-dbpedia-entity",
        "beir_scidocs": "beir-v1.0.0-scidocs",
        "beir_fever": "beir-v1.0.0-fever",
        "beir_climate_fever": "beir-v1.0.0-climate-fever",
        "beir_scifact": "beir-v1.0.0-scifact",
        # TREC
        "trec2019": "dl19-passage",
        "trec2020": "dl20",
    }
)
