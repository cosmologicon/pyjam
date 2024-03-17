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

# So-called golden divergence angle of phyllotaxis, around 137.5 deg.
phyllo = tau * (2 - phi)

# GLSL functions
def sign(x):
	return 1. if x > 0 else -1. if x < 0 else 0.
def clamp(x, a, b):
	return a if x < a else b if x > b else x
def mix(x, y, a):
	a = clamp(a, 0, 1)
	try:
		return tuple(b * (1 - a) + c * a for b, c in zip(x, y))
	except TypeError:
		return x * (1 - a) + y * a
def imix(x, y, a):
	a = clamp(a, 0, 1)
	try:
		return tuple(int(round(b * (1 - a) + c * a)) for b, c in zip(x, y))
	except TypeError:
		return int(round(x * (1 - a) + y * a))
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
	return math.sqrt(sum(a ** 2 for a in v))
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
	if dx < 0: return 1 - fade(-x, 0, -dx)
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
# Fade between function
def fadebetween(x, x0, y0, x1, y1):
	if x1 < x0: x1, y1, x0, y0 = x0, y0, x1, y1
	a = fade(x, x0, x1 - x0)
	return mix(y0, y1, a)
interp = fadebetween
def smoothfadebetween(x, x0, y0, x1, y1):
	if x1 < x0: x1, y1, x0, y0 = x0, y0, x1, y1
	a = smoothfade(x, x0, x1 - x0)
	return mix(y0, y1, a)
smoothinterp = smoothfadebetween
# Cycle between 0 and 1
def cycle(a):
	return 0.5 - 0.5 * math.cos(tau * a)

# Approach functions
def approach(x, target, dx):
	try:
		d = distance(x, target)
	except TypeError:
		d = abs(x - target)
	if d <= dx:
		return target
	return mix(x, target, dx / d)
def softapproach(x, target, dlogx, dxmax = float("inf"), dymin = 0.1):
	try:
		d = distance(x, target)
	except TypeError:
		d = abs(x - target)
	a = -math.expm1(-dlogx)
	if a * d > dxmax: a = dxmax / d
	if (1 - a) * d < dymin:
		return target
	return mix(x, target, a)


# Angular analogues - angles are treated modulo tau.
def dA(A):
	return (A + tau / 2) % tau - tau / 2
def mixA(A0, A1, a):
	return A1 if a >= 1 else A0 + dA(A1 - A0) * clamp(a, 0, 1)
def fadebetweenA(x, x0, A0, x1, A1):
	a = fadebetween(x, x0, 0, x1, 1)
	return mixA(A0, A1, a)
interpA = fadebetweenA
def smoothfadebetweenA(x, x0, A0, x1, A1):
	a = smoothfadebetween(x, x0, 0, x1, 1)
	return mixA(A0, A1, a)
smoothinterpA = smoothfadebetweenA
def approachA(A, targetA, deltaA):
	d = dA(targetA - A)
	if abs(d) <= deltaA: return targetA
	return A + deltaA * sign(d)
def softapproachA(A, targetA, dlogA, dAmax = float("inf"), dAmin = 0.01):
	d = abs(dA(targetA - A))
	a = -math.expm1(-dlogA)
	if a * d > dAmax: a = dAmax / d
	if (1 - a) * d < dAmin:
		return targetA
	return mixA(A, targetA, a)


# Log-space analogues
def mixL(xL, yL, a):
	return math.exp(mix(math.log(xL), math.log(yL), a))
def fadebetweenL(x, x0, yL0, x1, yL1):
	return math.exp(fadebetween(x, x0, math.log(yL0), x1, math.log(yL1)))
interpL = fadebetweenL
def smoothfadebetweenL(x, x0, yL0, x1, yL1):
	return math.exp(smoothfadebetween(x, x0, math.log(yL0), x1, math.log(yL1)))
smoothinterpL = smoothfadebetweenL
def approachL(xL, targetL, dx):
	return math.exp(approach(math.log(xL), math.log(targetL), dx))
def softapproachL(xL, targetL, dlogx, dxmax = float("inf"), dymin = 0.1):
	return math.exp(softapproach(math.log(xL), math.log(targetL), dlogx, dxmax, dymin))


# Polar coordinates
def CS(theta, r = 1, center = (0, 0)):
	return center[0] + r * math.cos(theta), center[1] + r * math.sin(theta)
def CSround(ntheta, r = 1, jtheta0 = 0, center = (0, 0)):
	return [CS((jtheta + jtheta0) / ntheta * tau, r, center) for jtheta in range(ntheta)]

# Rotation transform
def R(theta, v = None):
	C, S = CS(theta)
	if v is not None:
		x, y = v
		return C * x - S * y, S * x + C * y
	else:
		def R(v):
			x, y = v
			return C * x - S * y, S * x + C * y
		return R

# Deterministic pseudorandom
def fuzz(*args):
	a = 0.12
	for x in args:
		a += x + 3.45
		a *= 6.78
	return 91011.12 * math.sin(a) % 1

def fuzzrange(a, b, *args):
	return mix(a, b, fuzz(*args))


# Add to math module
_globals = dict(globals())
for k, v in _globals.items():
	if not k.startswith("_"):
		setattr(math, k, v)

