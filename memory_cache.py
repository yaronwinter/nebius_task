from collections import OrderedDict
import asyncio
import time

class MemoryCache:
    def __init__(self, maxsize=512, default_ttl=3600):
        self.store = OrderedDict()
        self.maxsize = maxsize
        self.default_ttl = default_ttl
        self.lock = asyncio.Lock()

    async def get(self, key):
        async with self.lock:
            item = self.store.get(key)
            if not item:
                return None
            value, expiry = item
            if expiry and time.time() > expiry:
                del self.store[key]
                return None
            self.store.move_to_end(key)
            return value

    async def set(self, key, value, ttl=None):
        ttl = ttl or self.default_ttl
        expiry = time.time() + ttl
        async with self.lock:
            self.store[key] = (value, expiry)
            self.store.move_to_end(key)
            if len(self.store) > self.maxsize:
                self.store.popitem(last=False)