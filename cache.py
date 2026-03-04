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

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.hits = 0
        self.misses = 0
        self.time = 0
    
    def request(self, item):
        self.time += 1
        if item in self.cache:
            self.hits += 1
            self.cache[item] = self.time
        else:
            self.misses += 1
            if len(self.cache) >= self.capacity:
                lru_item = min(self.cache, key=self.cache.get)
                del self.cache[lru_item]
            self.cache[item] = self.time
    
    def get_stats(self):
        return self.hits, self.misses

class OPTFFCache:
    def __init__(self, capacity, requests):
        self.capacity = capacity
        self.cache = set()
        self.hits = 0
        self.misses = 0
        self.requests = requests
        self.index = 0
    
    def request(self, item):
        if item in self.cache:
            self.hits += 1
        else:
            self.misses += 1
            if len(self.cache) >= self.capacity:
                farthest = max(self.cache, key=lambda x: self._next_use(x))
                self.cache.remove(farthest)
            self.cache.add(item)
        self.index += 1
    
    def _next_use(self, item):
        for i in range(self.index + 1, len(self.requests)):
            if self.requests[i] == item:
                return i
        return float('inf')
    
    def get_stats(self):
        return self.hits, self.misses

def compare_policies(capacity, requests):
    fifo = FIFOCache(capacity)
    lru = LRUCache(capacity)
    optff = OPTFFCache(capacity, requests)
    
    for req in requests:
        fifo.request(req)
        lru.request(req)
        optff.request(req)
    
    return {
        'FIFO': fifo.get_stats(),
        'LRU': lru.get_stats(),
        'OPTFF': optff.get_stats()
    }

if __name__ == '__main__':
    with open('input.txt') as f:
        k, m = map(int, f.readline().split())
        requests = list(map(int, f.readline().split()))
    
    results = compare_policies(k, requests)
    
    for policy, (hits, misses) in results.items():
        print(f"{policy}: {hits} hits, {misses} misses")
