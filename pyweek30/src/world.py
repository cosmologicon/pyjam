import math, random


R = 100

xhat = 1, 0, 0
yhat = 0, 1, 0
zhat = 0, 0, 1

spot0 = xhat, yhat, zhat

def neg(a):
	ax, ay, az = a
	return -ax, -ay, -az

nxhat = neg(xhat)
nyhat = neg(yhat)
nzhat = neg(zhat)

def times(a, c):
	ax, ay, az = a
	return c * ax, c * ay, c * az

def cross(a, b):
	ax, ay, az = a
	bx, by, bz = b
	return ay * bz - by * az, az * bx - bz * ax, ax * by - bx * ay

def plus(*vs):
	vxs, vys, vzs = zip(*vs)
	return sum(vxs), sum(vys), sum(vzs)

def linsum(*args):
	x, y, z = 0, 0, 0
	for j in range(0, len(args), 2):
		ax, ay, az = args[j]
		c = args[j+1]
		x += ax * c
		y += ay * c
		z += az * c
	return x, y, z

def avg(*vs):
	vxs, vys, vzs = zip(*vs)
	n = len(vs)
	return sum(vxs) / n, sum(vys) / n, sum(vzs) / n

# Rotate b about unit axis a
def rot(a, b, theta):
	proj = times(a, math.dot(a, b))
	perp = plus(b, neg(proj))
	z = cross(a, perp)
	C, S = math.CS(theta)
	return math.norm(linsum(proj, 1, perp, C, z, S), math.length(b))

# z projected onto the plane perpendicular to axis a
def perp(z, a):
	proj = times(a, math.dot(a, z))
	return plus(z, neg(proj))


def napproach(a, b, da):
	C, S = math.CS(min(da, 0.249 * math.tau))
	if math.dot(a, b) > C:
		return b
	c = math.norm(cross(math.norm(cross(a, b)), a))
	return math.norm(linsum(a, C, c, S))

def normal(face):
	a, b, c = face
	return math.norm(cross(plus(b, neg(a)), plus(c, neg(b))))


def usphere(n = 4):
	if n == 0:
		for x in [xhat, neg(xhat)]:
			for y in [yhat, neg(yhat)]:
				yield x, y, cross(x, y)
				yield y, x, cross(y, x)
		return
	for p0, p1, p2 in usphere(n - 1):
		q0 = math.norm(avg(p1, p2))
		q1 = math.norm(avg(p2, p0))
		q2 = math.norm(avg(p0, p1))
		yield q0, q1, q2
		yield p0, q2, q1
		yield p1, q0, q2
		yield p2, q1, q0


def spotrot(axis, spot, theta):
	return [rot(axis, vec, theta) for vec in spot]

def renorm(spot):
	f, l, u = spot
	u = math.norm(u)
	l = math.norm(cross(u, f))
	f = math.norm(cross(l, u))
	return f, l, u


targetrmoon = None

wspot = spot0
wrot = zhat


def act():
	global targetrmoon
	targetrmoon = math.norm(you)


def think(dt):
	global targetrmoon, wspot, wrot
	if targetrmoon is not None:
		state.rmoon = napproach(state.rmoon, targetrmoon, 0.6 * dt)
		if state.rmoon == targetrmoon:
			targetrmoon = None
	wrot = math.norm(plus(wrot, [1 * dt * random.uniform(-1, 1) for _ in range(3)]))
	wspot = renorm(spotrot([0, 0, 1], wspot, 0.1 * dt))
#	wspot = renorm(spotrot([0, 0, 1], wspot, 1 * dt))

