import random
import time
from functools import lru_cache

ARRAY_SIZE = 100_000
NUM_QUERIES = 50_000
CACHE_SIZE = 1000

array = [random.randint(1, 100) for _ in range(ARRAY_SIZE)]

queries = []
for _ in range(NUM_QUERIES):
    if random.random() < 0.7:
        l = random.randint(0, ARRAY_SIZE - 1)
        r = random.randint(l, ARRAY_SIZE - 1)
        queries.append(('Range', l, r))
    else:
        idx = random.randint(0, ARRAY_SIZE - 1)
        val = random.randint(1, 100)
        queries.append(('Update', idx, val))

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

@lru_cache(maxsize=CACHE_SIZE)
def range_sum_with_cache_internal(L, R):
    return sum(array[L:R+1])

def range_sum_with_cache(array, L, R):
    return range_sum_with_cache_internal(L, R)

def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache_internal.cache_clear()


def test_without_cache():
    for q in queries:
        if q[0] == 'Range':
            range_sum_no_cache(array, q[1], q[2])
        else:
            update_no_cache(array, q[1], q[2])

def test_with_cache():
    for q in queries:
        if q[0] == 'Range':
            range_sum_with_cache(array, q[1], q[2])
        else:
            update_with_cache(array, q[1], q[2])


if __name__ == '__main__':
    start = time.time()
    test_without_cache()
    no_cache_time = time.time() - start
    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")

    start = time.time()
    test_with_cache()
    with_cache_time = time.time() - start
    print(f"Час виконання з LRU-кешем: {with_cache_time:.2f} секунд")