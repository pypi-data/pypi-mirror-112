

class DictCache:

    def __init__(self, cache_size):
        self._cache_size = cache_size
        self._key_order_list = []
        self._cache_dict = {}

    def __getitem__(self, key):
        if self.is_cached(key):
            return self._cache_dict[key]
        else:
            raise KeyError(f"The specified key {key} is no cached")

    def is_cached(self, key) -> bool:
        return key in self._cache_dict

    def cache(self, key, value):
        if self.is_cached(key):
            self.uncache(key)

        self._key_order_list.append(key)
        self._cache_dict[key] = value

        self._handle_size()

    def uncache(self, key):
        self._key_order_list.remove(key)
        self._cache_dict.pop(key)

    def clear_cache(self):
        while len(self._cache_dict) > 0:
            first_key = self._key_order_list[0]
            self.uncache(first_key)

    def _handle_size(self):
        while len(self._cache_dict) > self._cache_size:
            first_key = self._key_order_list[0]
            self.uncache(first_key)
