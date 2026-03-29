
# https://github.com/cosmologicon/fuzz

import math, functools

CACHE_RESULTS = True

def hash(*args):
	a = 0.12
	for x in args:
		a += x + 3.45
		a *= 0.678
	return a

def random(*args):
	return 91011.12 * math.sin(hash(*args)) % 1

if CACHE_RESULTS:
    random = functools.lru_cache(1000000)(random)

def flip(p, *args):
    return random(*args) < p

def uniform(a, b, *args):
	return a + (b - a) * random(*args)

def randint(a, b, *args):
	x = int(math.floor(uniform(a, b + 1, *args)))
	return min(max(x, a), b)

def choice(values, *args):
	return values[randint(0, len(values) - 1, *args)]

def shuffle(values, *args):
	for j in range(len(values) - 1):
		k = randint(j, len(values) - 1, j, *args)
		if j != k:
			values[j], values[k] = values[k], values[j]
	return values

def shuffled(values, *args):
    return shuffle(list(values), *args)

