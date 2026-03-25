import math

def shrinkline(p0, p1, dp0, dp1, fmax = 0.3):
	d = math.distance(p0, p1)
	f0 = min(dp0 / d, fmax)
	f1 = min(dp1 / d, fmax)
	return math.mix(p0, p1, f0), math.mix(p0, p1, 1 - f1)

# https://www.reddit.com/r/algorithms/comments/9moad4/comment/e7gvsjv/
def cross(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 * y1 - x1 * y0
def vplus(p0, p1, f = 1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 + x1 * f, y0 + y1 * f
def vminus(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 - x1, y0 - y1
def orient(p0, p1, p2):
	return cross(vminus(p1, p0), vminus(p2, p0))
# Does the line segment (pA, pB) cross the line segment (pC, pD)
def linecross(seg0, seg1):
	pA, pB = seg0
	pC, pD = seg1
	return orient(pC, pD, pA) * orient(pC, pD, pB) < 0 and orient(pA, pB, pC) * orient(pA, pB, pD) < 0


