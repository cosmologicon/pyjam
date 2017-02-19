from __future__ import division

import collections


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
	return int(round(x * f))

