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
right = 0, 1, 0

def getlookat():
	camera = plus(you, times(up, 2), times(forward, -20))
	y = tuple(you)
	u = tuple(forward)
	return camera + y + u

def step(d):
	if d == 0:
		return
	global you, up, forward
	you = math.norm(plus(you, times(forward, R * math.tan(d / R))), R)
	up = math.norm(you)
	forward = math.norm(cross(up, right))

def rotate(a):
	if a == 0:
		return
	global forward, right
	C, S = math.CS(a)
	f0, r0 = forward, right
	forward = math.norm(plus(times(f0, C), times(r0, -S)))
	right = math.norm(plus(times(f0, S), times(r0, C)))



