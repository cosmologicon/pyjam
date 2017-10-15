# maff module: extend math module with convenience functions, by Christopher Night, CC0
# https://github.com/cosmologicon/maff

from __future__ import division
import math

__version__ = '0.1'
__versioninfo__ = (0, 1)

# Circle constant. Already available in 3.6+
tau = math.tau if hasattr(math, "tau") else 2 * math.pi

# Golden ratio
phi = (1 + math.sqrt(5)) / 2
Phi = phi - 1

# GLSL functions
def sign(x):
	return 1. if x > 0 else -1. if x < 0 else 0.
def clamp(x, a, b):
	return a if x < a else b if x > b else x
def mix(x, y, a):
	return x * (1 - a) + y * a
def step(edge, x):
	return float(x >= edge)
def smoothstep(edge0, edge1, x):
	if x >= edge1:
		return 1
	if x <= edge0:
		return 0
	a = (x - edge0) / (edge1 - edge0)
	return a * a * (3 - 2 * a)
def length(v):
	return math.sqrt(sum(a * a for a in v))
def distance(v0, v1):
	return math.sqrt(sum((a0 - a1) ** 2 for a0, a1 in zip(v0, v1)))
def dot(v0, v1):
	return sum(a * b for a, b in zip(v0, v1))

# Normalize with optional length
def normalize(v, r = 1):
	l = length(v)
	if l == 0:
		return [r] + [0] * (len(v) - 1)
	f = r / l
	return [a * f for a in v]
norm = normalize

# Equal to smoothstep(0, 1, x)
def ease(x):
	return 0 if x <= 0 else 1 if x >= 1 else x * x * (3 - 2 * x)

# Fade function
def fade(x, x0, dx):
	x -= x0
	if x <= 0: return 0
	if x >= dx: return 1
	return x / dx
# Equal to smoothstep(x0, x0 + dx, x)
def smoothfade(x, x0, dx):
	return ease(fade(x, x0, dx))
# Double fade function
def dfade(x, x0, x1, dx):
	return min(fade(x, x0, dx), 1 - fade(x, x1 - dx, dx))
def dsmoothfade(x, x0, x1, dx):
	return ease(dfade(x, x0, x1, dx))

# Approach functions
def approach(x, target, dx):
	try:
		d = distance(x, target)
		if d <= dx:
			return target
		return [mix(a, b, dx / d) for a, b in zip(x, target)]
	except TypeError:
		d = abs(x - target)
		if d <= dx:
			return target
		return mix(x, target, dx / d)
def softapproach(x, target, dlogx, dxmax = float("inf"), dymin = 0.1):
	try:
		d = distance(x, target)
		vector = True
	except TypeError:
		d = abs(x - target)
		vector = False
	f = -math.expm1(-dlogx)
	if f * d > dxmax: f = dxmax / d
	if (1 - f) * d < dymin: return target
	return [mix(a, b, f) for a, b in zip(x, target)] if vector else mix(x, target, f)


# Polar coordinates
def CS(theta, r = 1):
	return r * math.cos(theta), r * math.sin(theta)
def CSround(ntheta, r = 1, jtheta0 = 0):
	return [CS((jtheta + jtheta0) / ntheta * tau, r) for jtheta in range(ntheta)]

# Add to math module
_globals = dict(globals())
for k, v in _globals.items():
	if not k.startswith("_"):
		setattr(math, k, v)
