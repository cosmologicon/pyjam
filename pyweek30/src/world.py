import math


R = 100

xhat = 1, 0, 0
yhat = 0, 1, 0
zhat = 0, 0, 1

def neg(a):
	ax, ay, az = a
	return -ax, -ay, -az

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

def avg(*vs):
	vxs, vys, vzs = zip(*vs)
	n = len(vs)
	return sum(vxs) / n, sum(vys) / n, sum(vzs) / n

def napproach(a, b, da):
	C, S = math.CS(min(da, 0.249 * math.tau))
	if math.dot(a, b) > C:
		return b
	c = math.norm(cross(math.norm(cross(a, b)), a))
	return math.norm(plus(times(a, C), times(c, S)))



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


you = 0, 0, R
up = 0, 0, 1
forward = 1, 0, 0
left = 0, 1, 0

rmoon = 1, 0, 0
targetrmoon = None

ispot = forward, left, up



def step(d):
	if d == 0:
		return
	global you, up, forward
	you = math.norm(plus(you, times(forward, R * math.tan(d / R))), R)
	up = math.norm(you)
	forward = math.norm(cross(left, up))

def rotate(a):
	if a == 0:
		return
	global forward, left
	C, S = math.CS(a)
	f0, l0 = forward, left
	forward = math.norm(plus(times(f0, C), times(l0, S)))
	left = math.norm(plus(times(f0, -S), times(l0, C)))


def act():
	global ispot
	ispot = forward, left, up
	return
	global targetrmoon
	targetrmoon = math.norm(you)

def think(dt):
	global rmoon, targetrmoon
	if targetrmoon is not None:
		rmoon = napproach(rmoon, targetrmoon, 0.6 * dt)
		if rmoon == targetrmoon:
			targetrmoon = None

