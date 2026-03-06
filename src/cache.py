from collections import deque
import sys

class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = set()
        self.queue = deque()
        self.misses = 0
    
    def request(self, item):
        if item in self.cache:
            return
        self.misses += 1
        if len(self.cache) >= self.capacity:
            evicted = self.queue.popleft()
            self.cache.remove(evicted)
        self.cache.add(item)
        self.queue.append(item)

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.misses = 0
        self.time = 0
    
    def request(self, item):
        self.time += 1
        if item in self.cache:
            self.cache[item] = self.time
        else:
            self.misses += 1
            if len(self.cache) >= self.capacity:
                lru_item = min(self.cache, key=self.cache.get)
                del self.cache[lru_item]
            self.cache[item] = self.time

class OPTFFCache:
    def __init__(self, capacity, requests):
        self.capacity = capacity
        self.cache = set()
        self.misses = 0
        self.requests = requests
        self.index = 0
    
    def request(self, item):
        if item in self.cache:
            pass
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

def main():
    if len(sys.argv) != 2:
        print("Usage: python cache.py <input_file>")
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        k, m = map(int, f.readline().split())
        requests = list(map(int, f.readline().split()))
    
    fifo = FIFOCache(k)
    lru = LRUCache(k)
    optff = OPTFFCache(k, requests)
    
    for req in requests:
        fifo.request(req)
        lru.request(req)
        optff.request(req)
    
    print(f"FIFO  : {fifo.misses}")
    print(f"LRU   : {lru.misses}")
    print(f"OPTFF : {optff.misses}")

if __name__ == '__main__':
    main()
