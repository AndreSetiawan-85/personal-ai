import time

CACHE = {}
CACHE_EXPIRE = 300  # 5 menit


def get_cache(key):
    data = CACHE.get(key)

    if not data:
        return None

    created = data["time"]

    if time.time() - created > CACHE_EXPIRE:
        del CACHE[key]
        return None

    return data["value"]


def set_cache(key, value):
    CACHE[key] = {"time": time.time(), "value": value}
