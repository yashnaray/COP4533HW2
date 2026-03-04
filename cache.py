from collections import deque

class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = set()
        self.queue = deque()
        self.hits = 0
        self.misses = 0
    
    def request(self, item):
        if item in self.cache:
            self.hits += 1
        else:
            self.misses += 1
            if len(self.cache) >= self.capacity:
                evicted = self.queue.popleft()
                self.cache.remove(evicted)
            self.cache.add(item)
            self.queue.append(item)
    
    def get_stats(self):
        return self.hits, self.misses
