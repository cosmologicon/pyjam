import pygame, math
from . import render

C15, S15 = math.CS(math.radians(15))
C30, S30 = math.CS(math.radians(30))

def ptoline(p, n):
	pproj = math.dot(p, n)
	nx, ny = n
	proj = nx * pproj, ny * pproj
	return proj, math.distance(proj, p)

def scatter(ps):
	sps = [ps] + [tuple(render.R1(p) for p in ps)] + [tuple(render.R2(p) for p in ps)]
	sps = sps + [((x0, -y0), (x1, -y1)) for ((x0, y0), (x1, y1)) in sps]	
	sps = sps + [((-x0, y0), (-x1, y1)) for ((x0, y0), (x1, y1)) in sps]	
	return sps


class Shard:
	def __init__(self, pos, color, size):
		self.color = pygame.Color(color)
		self.size = size
		pos = self.constrain(pos, 0)
		self.anchors = [pos]

	def constrain(self, pos, j):
		if pos[1] < 0.0001:
			pos = pos[0], 0.0001
		if pos[0] < 0:
			pos = 0, pos[1]
#		if math.dot(pos, (S15, C15)) < 0:
#			return 0, 0
		if math.dot(pos, (C30, -S30)) > 0:
			pos, _ = ptoline(pos, (S30, C30))
		a = math.length(pos)
		w, h = self.size
		if a > 1 - h:
			pos = math.norm(pos, 1 - h)
		return pos

	def constrainanchor(self, j, pos):
		self.anchors[j] = self.constrain(pos, j)

	def sectordraw(self, simgs):
		sx, sy = self.anchors[0]
		sw, sh = self.size
		color0 = self.color
		color1 = render.dim(color0)
		for f, color in [(1, color1), (0.6, color0)]:
			S, C = math.norm((sx, sy), f)
			ps0 = [
				(sx + S * sh, sy + C * sh),
				(sx + C * sw, sy - S * sw),
				(sx - S * sh, sy - C * sh),
				(sx - C * sw, sy + S * sw),
			]
			render.sectorpoly(simgs, ps0, color)

	def colorat(self, pos):
		sx, sy = self.anchors[0]
		theta = math.atan2(sx, sy) if sx or sy else 0
		dx, dy = math.R(theta, pos)
		dy -= math.length((sx, sy))
		sw, sh = self.size
		if abs(dx / sw) + abs(dy / sh) < 1:
			return self.color
		return None

	def outlinesegs(self):
		sx, sy = self.anchors[0]
		sw, sh = self.size
		S, C = math.norm((sx, sy))
		ps = [
			(sx + S * sh, sy + C * sh),
			(sx + C * sw, sy - S * sw),
			(sx - S * sh, sy - C * sh),
			(sx - C * sw, sy + S * sw),
		]
		return [(ps[j], ps[(j+1)%4]) for j in range(4)]

	def drawoutline0(self, Fspot):
		for p0, p1 in self.outlinesegs():
			ps = render.cull(p0, p1)
			if not ps:
				continue
			render.drawlinesF(Fspot, ps, self.color)

	def drawoutline(self, Fspot):
		for p0, p1 in self.outlinesegs():
			ps = render.cull(p0, p1)
			if not ps:
				continue
			for sps in scatter(ps):
				render.drawlinesF(Fspot, sps, self.color)	

def fromspec(spec):
	if spec["type"] == "shard":
		return Shard(spec["pos"], spec["color"], spec["size"])

