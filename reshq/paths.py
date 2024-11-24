from pathlib import Path

CACHE_DIR = Path(__file__).parents[1].resolve()

LOG_DIR = CACHE_DIR / "logs"

CREATED_QUERY_CACHE_DIR = CACHE_DIR / "created_query_caches"

VALOUTPUT_DIR = CACHE_DIR / "valoutputs"
