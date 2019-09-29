try:
	from functools import lru_cache
except ImportError:
	class lru_cache:
		def __init__(self, size):
			if size is None: size = 10000000
			self.size = size
			self.cache = {}
			self.tcache = {}
			self.t = 0
		
		def __call__(self, func):
			self.func = func
			return self.call
		
		def call(self, *args, **kwargs):
			key = tuple(args) + tuple(sorted(tuple(kv) for kv in kwargs.items()))
			self.tcache[key] = self.t
			self.t += 1
			if key in self.cache:
				return self.cache[key]
			self.cache[key] = self.func(*args, **kwargs)
			if len(self.cache) > 2 * self.size:
				keys = sorted(self.cache, key = lambda k: self.tcache[k])
				self.cache = { k: self.cache[k] for k in keys[-self.size:] }
			return self.cache[key]
