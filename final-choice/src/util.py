from __future__ import division
import math


def clamp(x, a, b):
	return a if x < a else b if x > b else x

def norm(x, y, r = 1):
	if x == 0 and y == 0:
		return [r, 0]
	d = math.sqrt(x * x + y * y)
	return [r * x / d, r * y / d]

