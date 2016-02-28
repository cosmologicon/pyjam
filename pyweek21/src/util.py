import collections
from . import settings

f = None

def F(x, *z):
	if z:
		return tuple(int(round(f * a)) for a in (x,) + z)
	if isinstance(x, collections.Iterable):
		return tuple(int(round(f * a)) for a in x)
	return int(round(f * x))

def debug(*args):
	if not settings.DEBUG:
		return
	print(args)

