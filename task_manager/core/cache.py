import time
cache_store = {}

def set_cache(key, value, ttl = 10):
    cache_store[key] = {
        "value": value,
        "expiry": time.time() + ttl
    }

def get_cache(key):
    data = cache_store.get(key)

    if not data:
        return None
    
    if data["expiry"] < time.time():
        del cache_store[key]
        return None
    
    return data["value"]
