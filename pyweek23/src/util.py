from __future__ import division
import collections, math


# Height of the viewscreen.
h = 480

# Reference height of the viewscreen.
h0 = 480

f = h / h0

def seth(newh):
	global f, h
	h = newh
	f = h / h0

def F(x, *a):
	if a:
		return F([x] + list(a))
	if isinstance(x, (list, tuple)):
		return [int(round(y * f)) for y in x]
	return 0 if x == 0 else max(int(round(x * f)), 1) if x > 0 else min(int(round(x * f)), -1)

def clamp(x, a, b):
	return a if x < a else b if x > b else x

def norm(x, y, r = 1):
	if x == 0 and y == 0:
		return [r, 0]
	d = math.sqrt(x * x + y * y)
	return [r * x / d, r * y / d]

