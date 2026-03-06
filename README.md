# Cache Eviction Policies - COP4533 HW2

## Student Information

- **Name:** Yash Narayan
- **UFID:** 31198967

## Running

You will need a recent version of Python (tested with Python 3.x).

cache.py reads from the specified file. Example:

```bash
python src/cache.py examples/example.in
```

Example files are in the examples directory. There are three pairs of input and expected output files:

- example.in / example.out
- example2.in / example2.out
- example3.in / example3.out

## Input and Output

The input format is:

```
k m
r1 r2 r3 ... rm
```

where:

- k = cache capacity
- m = number of requests
- r1, ..., rm = integer request IDs

The output format is:

```
FIFO  : <number_of_misses>
LRU   : <number_of_misses>
OPTFF : <number_of_misses>
```

where the three policies are:

- FIFO = first-in-first-out
- LRU = least recently used
- OPTFF = Belady's farthest-in-future, optimal offline

## Comparison

Here are the number of misses reported for each policy when applied to the three example files:

| Input File | k  | m    | FIFO | LRU | OPTFF |
|------------|----|------|------|-----|-------|
| File1      | 5  | 50   | 34   | 33  | 24    |
| File2      | 20 | 500  | 208  | 205 | 97    |
| File3      | 35 | 1000 | 567  | 552 | 275   |

- OPTFF always has the fewest misses.
- The miss rates of FIFO and LRU are similar. This may be partially due to the fact that the access patterns in the example files are random, unlike real-world scenarios where some requests may be more frequent.

## Bad Cases for LRU/FIFO

For k = 3, it is possible for OPTFF to incur strictly fewer misses than LRU or FIFO. examples/example3.in is one such sequence. A simpler example is:

```
1 2 3 4 1 2 3 4
```

This results in 8 misses for LRU and FIFO, and 5 misses for OPTFF.

## Proof of OPTFF Optimality
Let A be an optimal offline algorithm that minimizes cache misses. Let (a1, ..., am) be the evictions made by A and (e1, ..., em) those made by OPTFF. Assume they differ and let i be the first index where ai != ei.

Up to step i, both algorithms have identical cache contents, so both ai and ei are present. Algorithm A could evict ei instead of ai without increasing misses.

Four cases cover all outcomes:

1. If ei is never accessed again, the change causes no additional misses.

2. If ei would be evicted after ai is accessed but before its next access, evict the same item that would have been evicted when ai was accessed. The item's cache lifetime only increases, so misses do not increase.

3. If ei would be evicted before either ei or ai is accessed, evict ai instead. Both end up absent from the cache, producing the same result.

4. Otherwise, both remain in the cache until their next access. Accessing ei changes from a hit to a miss, while accessing ai changes from a miss to a hit, so the total number of misses stays the same.

Thus replacing ai with ei does not increase misses. Repeating this exchange wherever A and OPTFF differ converts A into OPTFF without worsening performance. Therefore OPTFF is optimal.