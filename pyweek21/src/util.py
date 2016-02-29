import collections
from . import settings

f = None

def F(x, *z):
	if z:
		return tuple(F(a) for a in (x,) + z)
	if isinstance(x, collections.Iterable):
		return tuple(F(a) for a in x)
	return int(round(f * x)) if x <= 0 else max(int(round(f * x)), 1)

def debug(*args):
	if not settings.DEBUG:
		return
	print(" ".join(map(str, args)))

