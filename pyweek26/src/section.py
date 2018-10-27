# A section of the sewer

from __future__ import division
import math, pygame, random
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from . import graphics, thing, state, settings, view, sound

# A circular section without a current
# In this section the left and right arrow keys rotate you
class Pool():
	label = 'pool'
	rapid = 1
	fmode = None
	def __init__(self, pos, r, pressure0, drainable):
		self.pos = pos
		self.r = r
		self.pressure0 = pressure0
		self.drainable = drainable
		self.draining = False
		self.connections = []
		self.toturn = 0
		self.drainers = []  # pools above that are draining into this one
		self.hasfood = False
		self.whirl = 0
		self.final = False  # Is the final boss arena
		self.cansave = False
	def penter(self):
		return self.pos
	def pexit(self):
		return self.pos
	def pressure(self):
		return self.pressure0 - self.draining + len(self.drainers)
	def candrainfrom(self, obj):
		return self.drainable and not self.draining and self.dwall(obj) > self.r - 2
	def candropfrom(self, obj):
		return self.draining and self.dwall(obj) > self.r - 3
	def draintarget(self):
		# Pools directly below this one.
		pools = [s for s in state.sections if s.label == "pool" and s.dwall(self) > 0 and s.pos.z < self.pos.z]
		assert pools, "Drainable pool at %s not above another pool!" % (self.pos,)
		return max(pools, key=lambda pool: pool.pos.z)
	def drain(self, you=None):
		self.draining = True
		if you is not None:
			self.drop(you)
		dt = self.draintarget()
		sound.manager.PlaySound('drain')
		state.animation.waterfalls.append(graphics.Waterfall([self.pos[0],self.pos[1],self.pos[2]],dt,self.pos[2]-dt.pos[2]))
		state.effects.append(thing.Waterfall(self, dt))
		dt.drainers.append(self)
	def drop(self, you):
		you.landed = False
		you.toleap = 0
		you.section = self.draintarget()
	def canfeed(self, you):
		return state.food < state.foodmax and self.hasfood and self.dwall(you) > self.r / 2
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
		you.v = math.approach(you.v, v, 200 * dt)
		if self.candropfrom(you):
			self.drop(you)
		if self.canfeed(you):
			state.food = state.foodmax
			sound.manager.PlaySound('food_got')
	def atilt(self, you):
		return Vector3(0, 0, 0)
	def act(self, you):
		if self.candrainfrom(you):
			self.drain(you)
			return True
		return False
	def flow(self, dt, obj):
		obj.pos += dt * self.vflow(obj.pos)
	def vflow(self, pos):
		# Very gentle flow toward the center
		v = (self.pos - pos) / 10
		if v.length() > 1:
			v = v.normalize()
		if self.final:
			self.whirl = [2, 4, 6, 8, 9, 10, 11][len(self.drainers)]
		if self.draining or self.whirl != 0:
			v *= 4
		if self.whirl != 0:
			dpos = pos - self.pos
			dpos.z = 0
			d = dpos.length() / self.r
			if d > 0:
				v += pygame.math.Vector3(0, 0, 1).cross(dpos).normalize() * self.whirl
		# Waterfalls push you away
		if not self.draining:
			for drainer in self.drainers:
				dpos = pos - drainer.pos
				dpos.z = 0
				d = dpos.length() / 6
				if 0 < d < 1:
					v += dpos.normalize() * (1 - d) ** 2 * 12
		return v
	# Distance above the water level - negative for underwater
	def dzwater(self, pos):
		return pos.z - self.pos.z
	# Distance from wall - negative for objects outside
	def dwall(self, obj):
		d = obj.pos - self.pos
		d.z = 0
		return self.r - d.length()
	def acquires(self, obj):
		return self.dwall(obj) > 2
	def influence(self, obj):
		return math.clamp(self.dwall(obj) / 2, 0, 1)
	def handoff(self, obj):
		if self.dwall(obj) < 1 and self.connections:
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
		glBegin(GL_POLYGON) # replaced by drawmodel_sect_pool
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
		# Food fountain
		if self.hasfood:
			glColor4f(1, 0, 1, 1)
			glPointSize(2)
			glBegin(GL_POINTS)
			for jfood in range(50):
				x, y = math.CS(jfood * math.phi, self.r / 2 * (jfood ** 2 * math.phi % 1))
				z = 3 * ((jfood ** 3 * math.phi + pygame.time.get_ticks() * 0.001) % 1) ** 2
				glVertex(x, y, z)
			glEnd()
		glPopMatrix()
	def drawmap(self):
		graphics.drawdisk(self.pos, self.r, state.mapcolor(self.sectionid))
		graphics.drawdisk(self.pos + pygame.math.Vector3(0, 0, -1), self.r + 1, (0, 0, 0, 1))
	def spawn(self, dt):
		pass

class Pipe():
	label = 'pipe'
	rapid = 1
	fmode = None
	def __init__(self, pos0, pos1, width = 1):
		self.pos0 = 1 * pos0
		self.pos1 = 1 * pos1
		self.pos = (self.pos0 + self.pos1) / 2
		self.rate = 20
		self.width = width
		d = self.pos1 - self.pos0
		self.face = d.normalize()
		self.length = d.length()
		self.angle = math.atan2(self.face.x, self.face.y)
		self.connections = []
	# Distance to the section center line, in units of the width.
	def dcenter(self, pos):
		p = pos - self.pos0
		proj = p.dot(self.face) * self.face
		return (p - proj).length() / self.width / 1.4  # Pipes have a wider influence than they appear
	# Distance along the line
	def afactor(self, pos):
		return (pos - self.pos0).dot(self.face) / self.length
	def move(self, you, dt, dx, dy, turn):
		heading = self.angle
		you.heading = math.anglesoftapproach(you.heading, heading, 50 * dt, dymin = 0.01)
		you.v = pygame.math.Vector3(0, 0, 0)
	def atilt(self, you):
		return Vector3(0, 0, 0)
	def act(self, you):
		return False
	def flow(self, dt, obj):
		v = self.vflow(obj.pos)
		obj.pos += dt * v
	def vflow(self, pos):
		return self.face * self.rate
	def handoff(self, obj):
		# Just drops you off as soon as you're beyond the bottom pool.
		pool0, pool1 = self.connections
		if pool0.dwall(obj) < 0:
			state.food -= 1
			obj.section = self.connections[1]
			obj.pos = 1 * obj.section.pos
			view.addsnap(0.5)
			obj.pos.z -= 3
			state.animation.splashes.append(graphics.Splashes([obj.section.pos[0],obj.section.pos[1],obj.section.pos[2]], obj.section, lifetime=60))
			sound.manager.PlaySound('gurgle001')

	def dzwater(self, pos):
		return pos.z - self.connections[0].pos.z
	def constrain(self, obj):
		p = obj.pos - self.pos0
		a = p.dot(self.face)
		d0 = a * self.face + self.pos0
		d = obj.pos - d0
		dmax = self.width - obj.r
		if d.length() > dmax:
			obj.pos = d0 + dmax * d.normalize()
	def acquires(self, obj):
		return state.food > 0 and 0 < self.afactor(obj.pos) < 1
	def influence(self, obj):
		return 0
	def draw(self):
		glPushMatrix()
		glTranslate(*self.pos0)
		glRotate(90 + math.degrees(-self.angle), 0, 0, 1)
		if settings.debug_graphics:
			glTranslate(self.length - 2, 0, 0)
			glRotate(90, 0, 1, 0)
			graphics.drawcylinder((0, 0, 0), self.width, h = 2, color = [0.4, 0.4, 0.4, 1])
		glPopMatrix()
	def spawn(self, dt):
		return

	def drawmap(self):
		pass

class Connector():
	rapid = 1
	fmode = None
	def setpools(self):
		self.pool0 = self
		while self.pool0.label != "pool":
			self.pool0 = self.pool0.connections[0]		
		self.pool1 = self
		while self.pool1.label != "pool":
			self.pool1 = self.pool1.connections[1]		
	def getflowrate(self):
		if self.pool0.pos.z > self.pool1.pos.z:
			rate = 10
		elif self.pool0.pos.z < self.pool1.pos.z:
			rate = -10
		else:
			dpressure = self.pool0.pressure() - self.pool1.pressure()
			rate = 5 * dpressure
		return rate * self.rapid
	# Speed with respect to the current that the player swims while pressing these buttons
	def swimrate(self, dx, dy):
		ax = 5 + 10 * (self.rapid - 1)
		return pygame.math.Vector3(ax * dx, 3 + 5 * dy, 0)
	def drawmap(self):
		pass
	
class StraightConnector(Connector):
	label = 'straight'
	def __init__(self, pos0, pos1, width = 4):
		self.pos0 = pos0
		self.pos1 = pos1
		self.pos = (self.pos0 + self.pos1) / 2
		self.width = width
		d = self.pos1 - self.pos0
		self.face = d.normalize()
		self.length = d.length()
		self.dz = d.z
		self.dl = (d - pygame.math.Vector3(0, 0, self.dz)).length()
		self.aslope = math.atan2(self.dz, self.dl)
		self.angle = math.atan2(self.face.x, self.face.y)
		self.connections = []
		self.blockers = []
		self.right = self.face.cross(pygame.math.Vector3(0, 0, 1)).normalize()
		self.ps = [
			self.pos0 + self.width * self.right,
			self.pos1 + self.width * self.right,
			self.pos1 - self.width * self.right,
			self.pos0 - self.width * self.right,
		]
		
		dw = 1  # outline width
		self.ops = [
			self.pos0 + (self.width + dw) * self.right + pygame.math.Vector3(0, 0, -1),
			self.pos1 + (self.width + dw) * self.right + pygame.math.Vector3(0, 0, -1),
			self.pos1 - (self.width + dw) * self.right + pygame.math.Vector3(0, 0, -1),
			self.pos0 - (self.width + dw) * self.right + pygame.math.Vector3(0, 0, -1),
		]
		
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
		v = self.swimrate(dx, dy).rotate_z(math.degrees(-heading))
		
		you.v = pygame.math.Vector3(math.approach(you.v, v, 200 * dt))
	def atilt(self, you):
		return math.degrees(self.aslope) * self.right
	def act(self, you):
		return False

	def dzwater(self, pos):
		# Not exactly right for slopes but probably close enough.
		return pos.z - (self.pos0.z + self.dz * self.afactor(pos))
	def flow(self, dt, obj):
		v = self.vflow(obj.pos)
		for c in self.connections:
			v = math.mix(v, c.vflow(obj.pos), c.influence(obj))
		obj.pos += dt * v
	def vflow(self, pos):
		return self.face * self.getflowrate()

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
		return -0.1 <= self.afactor(obj.pos) < 1.1
	def influence(self, obj):
		return 0
	def draw(self):
		glPushMatrix()
		glColor4f(0, 0, 1, 0.3)
		glTranslate(*self.pos0)
		glRotate(math.degrees(-self.angle), 0, 0, 1)
		if settings.debug_graphics:
			glBegin(GL_QUADS) # replaced by drawmodel_sect_straight
			for dx, dy in [(-1, 0), (-1, 1), (1, 1), (1, 0)]:
				glVertex(dx * self.width, dy * self.dl, dy * self.dz)
			glEnd()
		for blocker in self.blockers:
			w = int(round(self.width)) - 1
			y = blocker.afactor * self.length
			for x in range(-w, w+1):
				z = math.sqrt(self.width ** 2 - x ** 2)
				#p0 = x + 0.25 * dx, y, 0
				p0 = x + 0.25 * 1, y, 0
				graphics.drawcylinder(p0, 0.25, z, [0.3, 0.3, 0.3, 1])
		glColor4f(0.8, 0.8, 0.8, 1)
		n = int(math.ceil(self.length / 4))
		for jball in range(n+1):
			y = jball / n * self.length
			z = jball / n * self.dz
			for x in (-self.width, self.width):
				glPushMatrix()
				glTranslate(x, y, z)
				graphics.drawsphere(0.3)
				glPopMatrix()
		glPopMatrix()
	def drawmap(self):
		glColor(*state.mapcolor(self.sectionid))
		glBegin(GL_QUADS)
		for p in self.ps:
			glVertex(*p)
		glEnd()
		glColor(0, 0, 0, 0)
		glBegin(GL_QUADS)
		for p in self.ops:
			glVertex(*p)
		glEnd()
		
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

# TODO: I'm 90% sure this class doesn't need to exist.
class SlopeConnector(StraightConnector):
	label = 'slope'

class CurvedConnector(Connector):
	label = 'curve'
	def __init__(self, p0, p1, center, beta, right, R, rate = 10, width = 4):
		self.R = R
		self.rate = rate
		self.width = width
		self.beta = beta
		self.p0 = p0
		self.p1 = p1
		self.pos = (self.p0 + self.p1) / 2
		self.center = center
		# TODO: might fail if beta > tau/4
		self.n = ((self.p0 + self.p1) / 2 - self.center).normalize()
		self.right = right
		self.z = pygame.math.Vector3(0, 0, (1 if self.right else -1))  # Upward for rightward turns

		self.vertices = []
		nseg = int(math.ceil(self.beta * 6))
		angles = [360 + math.degrees(jseg / nseg * self.beta) for jseg in range(-nseg, nseg + 1)]
		ds = [self.n.rotate(-angle, self.z) for angle in angles]
		self.vertices = [d * (self.R - self.width) for d in ds] + [d * (self.R + self.width) for d in ds[::-1]]
#		self.pB = pB
		self.connections = []

		alpha = math.atan2(self.n.x, self.n.y)
		self.mapstart = math.degrees(alpha - self.beta)
		self.mapsweep = math.degrees(2 * self.beta)
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
		v = self.swimrate(dx, dy).rotate_z(math.degrees(-heading))
		you.v = pygame.math.Vector3(math.approach(you.v, v, 200 * dt))
	def atilt(self, you):
		r = you.pos - self.center
		if r.length() < 6:
			r.scale_to_length(6)
		v = self.vflow(you.pos)
		u = r.cross(Vector3(0, 0, 1)).normalize()
		a = -abs(v.cross(r).z * (v.length() / r.length_squared()))
		return u * 25 * math.tanh(a * 0.1)
	def act(self, you):
		return False

	def dzwater(self, pos):
		return pos.z - self.p0.z
	def flow(self, dt, obj):
		obj.pos += dt * self.vflow(obj.pos)
	def vflow(self, pos):
		p = pos - self.center
		speed = self.getflowrate() * p.length() / self.R
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
		pmin = self.R - (self.width - obj.r)
		pmax = self.R + (self.width - obj.r)
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
		glBegin(GL_POLYGON) # replaced by drawmodel_sect_curve
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

#		glPushMatrix()
#		glTranslate(*self.pB)
#		glColor4f(0.8, 0, 0, 1)
#		graphics.drawsphere(0.6)
#		glPopMatrix()
		# not needed anymore: calls made directly in gamescene
		#if not settings.debug_graphics:
		#	graphics.drawmodel_sect_curve(self)
		
	def drawmap(self):
		glPushMatrix()
		glColor4f(*state.mapcolor(self.sectionid))
		glTranslate(*self.center)
		r0 = self.R - self.width
		r1 = self.R + self.width
		gluPartialDisk(graphics.quadric, r0, r1, 40, 1, self.mapstart, self.mapsweep)
		glColor4f(0, 0, 0, 1)
		glTranslate(0, 0, -1)
		gluPartialDisk(graphics.quadric, r0 - 1, r1 + 1, 40, 1, self.mapstart, self.mapsweep)
		glPopMatrix()
	def spawn(self, dt):
		pass

"""
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
"""

