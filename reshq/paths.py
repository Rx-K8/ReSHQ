from pathlib import Path

CACHE_DIR = Path(__file__).parents[1].resolve()

LOG_DIR = CACHE_DIR / "logs"

CREATED_QUERY_CACHE_FILE = CACHE_DIR / "created_query_cache.json"
