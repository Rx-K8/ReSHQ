from types import MappingProxyType

TOPICS = MappingProxyType(
    {
        # BEIR(Benchmarking IR)
        "beir_climate_fever": "beir-v1.0.0-climate-fever",
        # TREC
        "trec2019": "dl19-passage",
        "trec2020": "dl20",
    }
)
