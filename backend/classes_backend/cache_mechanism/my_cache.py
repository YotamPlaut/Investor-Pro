from backend.classes_backend.stock import Stock


class MyCache:

    def __init__(self, size=3):
        self.size = size
        self.cache = []

    def add_item(self, item: Stock):
        if len(self.cache) >= self.size:
            self.cache.pop(0)
        self.cache.append(item)

    def is_stock_index_in_cache(self, stock_index: int):
        i = 0
        for item in self.cache:
            if stock_index == item.stock_index:
                return True, i
            i += 1

        return False, -1

    def get_item(self, stock_index):

        is_in_cache, index = self.is_stock_index_in_cache(stock_index)
        if is_in_cache:
            return self.cache[index]

        return None

    def remove_item(self, index: int):
        if 0 <= index < len(self.cache):
            self.cache.pop(index)

