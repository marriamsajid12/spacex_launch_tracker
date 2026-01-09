import json
import time
from pathlib import Path
from typing import Any, Optional

CACHE_DIR = Path("data")
CACHE_TTL = 24 * 60 * 60  # 24 hours

try:
    CACHE_DIR.mkdir(exist_ok=True)
except Exception as e:
    print(f"Error creating cache directory '{CACHE_DIR}': {e}")


def load_cache(name: str) -> Optional[Any]:
    """
    Load cached data from a JSON file.
    Returns None if the cache is missing, expired, or invalid.
    """
    file_path = CACHE_DIR / f"{name}.json"

    try:
        if not file_path.exists():
            return None

        if time.time() - file_path.stat().st_mtime > CACHE_TTL:
            return None

        return json.loads(file_path.read_text())

    except Exception as e:
        print(f"Error loading cache '{file_path}': {e}")
        return None


def save_cache(name: str, data: Any) -> None:
    """
    Save data to a JSON cache file.
    """
    file_path = CACHE_DIR / f"{name}.json"

    try:
        file_path.write_text(json.dumps(data))
    except Exception as e:
        print(f"Error saving cache '{file_path}': {e}")
