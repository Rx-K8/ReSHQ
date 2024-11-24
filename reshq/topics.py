from types import MappingProxyType

TOPICS = MappingProxyType(
    {
        # BEIR(Benchmarking IR)
        "beir_trec_covid": "beir-v1.0.0-trec-covid-test",
        # TREC
        "trec2019": "dl19-passage",
        "trec2020": "dl20",
    }
)
