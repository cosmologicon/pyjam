# A section of the sewer

from __future__ import division
import math, pygame, random
from OpenGL.GL import *
from . import graphics, thing, state

# A circular section without a current
# In this section the left and right arrow keys rotate you
class Pool():
	def __init__(self, pos, r):
		self.pos = pos
		self.r = r
		self.connections = []
		self.toturn = 0
	def penter(self):
		return self.pos
	def pexit(self):
		return self.pos

	def move(self, you, dt, dx, dy, turn):
		if turn:
			you.heading += self.toturn
			self.toturn = math.tau / 2
		you.heading += 2 * dt * dx
		if self.toturn:
			toturn = math.softapproach(self.toturn, 0, 10 * dt, dymin = 0.01)
			you.heading += self.toturn - toturn
			self.toturn = toturn
		speed = 10 if dy > 0 else -3 if dy < 0 else 0
		v = pygame.math.Vector3(0, speed, 0).rotate_z(math.degrees(-you.heading))
		you.v = math.approach(you.v, v, 50 * dt)

	def flow(self, dt, obj):
		# Very gentle flow toward the center
		obj.pos += dt * self.vflow(obj.pos)
	def vflow(self, pos):
		v = (self.pos - pos) / 10
		if v.length() > 1:
			v = v.normalize()
		return v
	def acquires(self, obj):
		return (obj.pos - self.pos).length() < self.r - 2
	def influence(self, obj):
		d = (obj.pos - self.pos).length()
		return math.clamp((self.r - d) / 2, 0, 1)
	def handoff(self, obj):
		d = (obj.pos - self.pos).length()
		if d > self.r - 1 and self.connections:
			paths = [c for c in self.connections if c.acquires(obj)]
			if paths:
				path = min(paths, key = lambda c: c.dcenter(obj.pos))
				if path.dcenter(obj.pos) < 1:
					obj.section = path
					obj.upstream = obj.face.dot(path.face) < 0
					self.toturn = 0
	def constrain(self, obj):
		p = obj.pos - self.pos
		pmax = self.r - obj.r
		if p.length() > pmax:
			obj.pos = self.pos + pmax * p.normalize()
	def draw(self):
		glPushMatrix()
		glColor4f(0, 0, 1, 0.3)
		glTranslate(*self.pos)
		glBegin(GL_POLYGON)
		for x, y in math.CSround(int(round(10 * self.r)), r = self.r):
			glVertex(x, y, 0)
		glEnd()
		# Fixed barriers
		glColor4f(0.8, 0.8, 0.8, 1)
		for x, y in math.CSround(int(round(2 * self.r)), r = self.r):
			glPushMatrix()
			glTranslate(x, y, 0)
			graphics.drawsphere(0.2)
			glPopMatrix()
		glPopMatrix()
	def spawn(self, dt):
		pass


class StraightConnector():
	def __init__(self, pos0, pos1, rate = 10, width = 4):
		self.pos0 = pos0
		self.pos1 = pos1
		self.rate = rate
		self.width = width
		d = self.pos1 - self.pos0
		self.face = d.normalize()
		self.length = d.length()
		self.angle = math.atan2(self.face.x, self.face.y)
		self.connections = []
		self.blockers = []
	# Distance to the section center line, in units of the width.
	def dcenter(self, pos):
		p = pos - self.pos0
		proj = p.dot(self.face) * self.face
		return (p - proj).length() / self.width
	# Distance along the line
	def afactor(self, pos):
		return (pos - self.pos0).dot(self.face) / self.length
	def move(self, you, dt, dx, dy, turn):
		if turn:
			you.upstream = not you.upstream
		heading = self.angle + (math.tau / 2 if you.upstream else 0)
		you.heading = math.anglesoftapproach(you.heading, heading, 10 * dt, dymin = 0.01)
		v = pygame.math.Vector3(5 * dx, 10 + 12 * dy, 0).rotate_z(math.degrees(-heading))
		
		you.v = pygame.math.Vector3(math.approach(you.v, v, 50 * dt))

	def flow(self, dt, obj):
		v = self.vflow(obj.pos)
		for c in self.connections:
			v = math.mix(v, c.vflow(obj.pos), c.influence(obj))
		obj.pos += dt * v
	def vflow(self, pos):
		return self.face * self.rate

	def handoff(self, obj):
		for connection in self.connections:
			if connection.acquires(obj):
				obj.section = connection
	def constrain(self, obj):
		p = obj.pos - self.pos0
		a = p.dot(self.face)
		d0 = a * self.face + self.pos0
		d = obj.pos - d0
		dmax = self.width - obj.r
		if d.length() > dmax:
			obj.pos = d0 + dmax * d.normalize()
		for blocker in self.blockers:
			a0 = blocker.afactor * self.length
			da = a - a0
			if 0 <= da < obj.r:
				obj.pos += self.face * (obj.r - da)
			elif -obj.r < da < 0:
				obj.pos -= self.face * (obj.r + da)
	def acquires(self, obj):
		return 0 <= self.afactor(obj.pos) < 1
	def influence(self, obj):
		return 0
	def draw(self):
		glPushMatrix()
		glColor4f(0, 0, 1, 0.3)
		glTranslate(*self.pos0)
		glRotate(math.degrees(-self.angle), 0, 0, 1)
		glBegin(GL_QUADS)
		for dx, dy in [(-1, 0), (-1, 1), (1, 1), (1, 0)]:
			glVertex(dx * self.width, dy * self.length, 0)
		glEnd()
		for blocker in self.blockers:
			w = int(round(self.width)) - 1
			y = blocker.afactor * self.length
			for x in range(-w, w+1):
				z = math.sqrt(self.width ** 2 - x ** 2)
				p0 = x + 0.25 * dx, y, 0
				graphics.drawcylinder(p0, 0.25, z, [0.3, 0.3, 0.3, 1])
		glColor4f(0.8, 0.8, 0.8, 1)
		n = int(round(self.length / 4))
		for jball in range(n+1):
			y = jball / n * self.length
			for x in (-self.width, self.width):
				glPushMatrix()
				glTranslate(x, y, 0)
				graphics.drawsphere(0.3)
				glPopMatrix()
		glPopMatrix()
	def spawn(self, dt):
		return
		if isinstance(self.connections[0], Pool) and random.uniform(0, 0.5) < dt:
			obj = thing.Debris()
			obj.section = self
			d = self.width - obj.r
			obj.pos = self.pos0 + random.uniform(-d, d) * self.face.rotate_z(90)
			while self.connections[0].acquires(obj):
				obj.pos += 0.1 * self.vflow(obj.pos)
			for _ in range(3):
				obj.pos += 0.1 * self.vflow(obj.pos)
			state.objs.append(obj)

class CurvedConnector():
	def __init__(self, pA, pB, pC, r, rate = 10, width = 4):
		self.r = r
		self.rate = rate
		self.width = width
		face0 = (pB - pA).normalize()
		face1 = (pC - pB).normalize()
		self.beta = 1/2 * math.acos(face0.dot(face1))
		self.d = self.r * math.tan(self.beta)
		self.p0 = pB - face0 * self.d
		self.p1 = pB + face1 * self.d
		self.n = (face0 - face1).normalize()
		self.z = face1.cross(face0).normalize()  # Upward for rightward turns
		self.right = self.z.z > 0
		self.center = self.p0 + self.r * face0.cross(self.z)

		self.vertices = []
		nseg = int(math.ceil(self.beta * 6))
		angles = [360 + math.degrees(jseg / nseg * self.beta) for jseg in range(-nseg, nseg + 1)]
		ds = [self.n.rotate(-angle, self.z) for angle in angles]
		self.vertices = [d * (self.r - self.width) for d in ds] + [d * (self.r + self.width) for d in ds[::-1]]
		self.pB = pB
		self.connections = []
	def penter(self):
		return self.p0
	def pexit(self):
		return self.p1

	def keeps(self, obj):
		p = obj.pos - self.center
		return p.dot(self.n) > p.length() * math.cos(self.beta)
	def move(self, you, dt, dx, dy, turn):
		if turn:
			you.upstream = not you.upstream
		p = you.pos - self.center
		if not self.right:
			p *= -1
		angle = math.atan2(p.y, -p.x)
		heading = angle + (math.tau / 2 if you.upstream else 0)
		you.heading = math.anglesoftapproach(you.heading, heading, 10 * dt, dymin = 0.01)
		v = pygame.math.Vector3(5 * dx, 10 + 12 * dy, 0).rotate_z(math.degrees(-heading))
		you.v = pygame.math.Vector3(math.approach(you.v, v, 50 * dt))

	def flow(self, dt, obj):
		obj.pos += dt * self.vflow(obj.pos)
	def vflow(self, pos):
		p = pos - self.center
		speed = self.rate * p.length() / self.r
		return p.cross(self.z).normalize() * speed

	def handoff(self, obj):
		if self.keeps(obj): return
		for connection in self.connections:
			if connection.acquires(obj):
				obj.section = connection
	def acquires(self, obj):
		return self.keeps(obj)
	def influence(self, obj):
		return 0
	def constrain(self, obj):
		p = obj.pos - self.center
		pmin = self.r - (self.width - obj.r)
		pmax = self.r + (self.width - obj.r)
		if p.length() < pmin:
			obj.pos = self.center + pmin * p.normalize()
		if p.length() > pmax:
			obj.pos = self.center + pmax * p.normalize()
	def draw(self):
		glPushMatrix()
		glColor4f(0, 0, 1, 0.3)
		glTranslate(*self.center)
#		angle = math.atan2(self.n.x, self.n.y)
#		glRotate(math.degrees(angle), 0, 0, 1)
		glBegin(GL_POLYGON)
		for vertex in self.vertices:
			glVertex(*vertex)
		glEnd()
		glColor4f(0.8, 0.8, 0.8, 1)
		for vertex in self.vertices:
			glPushMatrix()
			glTranslate(*vertex)
			graphics.drawsphere(0.2)
			glPopMatrix()
		glColor4f(0.8, 0, 0, 1)
		graphics.drawsphere(0.6)
		glPopMatrix()

		glPushMatrix()
		glTranslate(*self.pB)
		glColor4f(0.8, 0, 0, 1)
		graphics.drawsphere(0.6)
		glPopMatrix()
	def spawn(self, dt):
		pass

def connectpools(pool0, pool1, rate = 10, width = 4, r = 10, waypoints = []):
	ps = [pool0.pos] + waypoints + [pool1.pos]
	curves = [
		CurvedConnector(ps[j], ps[j+1], ps[j+2], r, rate = rate, width = width)
		for j in range(len(ps) - 2)
	]
	cs = [pool0] + curves + [pool1]
	straights = [
		StraightConnector(cs[j].pexit(), cs[j+1].penter(), rate = rate, width = width)
		for j in range(len(cs) - 1)
	]
	segs = []
	for c, straight in zip(cs[:-1], straights):
		segs.append(c)
		segs.append(straight)
	segs.append(cs[-1])
	for jseg in range(len(segs) - 1):
		seg0, seg1 = segs[jseg], segs[jseg + 1]
		seg0.connections.append(seg1)
		seg1.connections.append(seg0)
	return segs[1:-1]

