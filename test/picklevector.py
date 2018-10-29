from __future__ import print_function
import pygame, random

try:
	import cPickle as pickle
except ImportError:
	import pickle

pfilename = "/tmp/vector.pkl"

class obj:
	def __init__(self):
		self.v = pygame.math.Vector3(random.random(), random.random(), random.random())

objs = [obj() for _ in range(100)]
pickle.dump(objs, open(pfilename, "wb"))
objs1 = pickle.load(open(pfilename, "rb"))
print([o.v for o in objs1])


