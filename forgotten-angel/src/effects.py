import pygame, math, random
import state, img, vista

class Explosion(object):
	imgname = "boom"
	lifetime = 1
	def __init__(self, parent, v = (0, 0)):
		self.x, self.y = parent.x, parent.y
		self.vx, self.vy = v
		self.t = 0
		self.imgname = "smoke%s" % random.choice(range(4))
		self.angle = random.uniform(0, math.tau)
	
	def think(self, dt):
		self.t += dt
		self.x += dt * self.vx
		self.y += dt * self.vy
		if self.t > self.lifetime:
			state.state.effects.remove(self)
			
	def draw(self):
		scale = 1 + 2 * self.t / self.lifetime
		alpha = 1 - self.t / self.lifetime
		img.worlddraw(self.imgname, (self.x, self.y), self.angle, scale = scale, alpha = alpha)

class Laser(object):
	lifetime = 0.4

	def __init__(self, obj0, obj1, color):
		self.obj0, self.obj1 = obj0, obj1
		self.t = 0
		self.color = color
	
	def think(self, dt):
		self.t += dt
		if self.t > self.lifetime:
			state.state.effects.remove(self)
			
	def draw(self):
		p0 = vista.worldtoscreen((self.obj0.x, self.obj0.y))
		p1 = vista.worldtoscreen((self.obj1.x, self.obj1.y))
		pygame.draw.line(vista.screen, self.color, p0, p1)

class Bullet(object):
	v = 10
	r = 0.05
	color = 100, 100, 100

	def __init__(self, obj0, obj1, damage):
		self.obj0 = obj0
		self.obj1 = obj1
		self.x = self.obj0.x
		self.y = self.obj0.y
		self.D = math.sqrt((self.obj1.x - self.obj0.x) ** 2 + (self.obj1.y - self.obj0.y) ** 2)
		self.damage = damage
		self.t = 0

	def think(self, dt):
		self.t += dt
		self.D -= self.v * dt
		if self.D <= 0:
			self.obj1.takedamage(self.damage)
			state.state.effects.remove(self)
		dx, dy = self.obj0.x - self.obj1.x, self.obj0.y - self.obj1.y
		d = math.sqrt(dx ** 2 + dy ** 2)
		self.x = self.obj1.x + dx * self.D / d
		self.y = self.obj1.y + dy * self.D / d

	def draw(self):
		screenpos = vista.worldtoscreen((self.x, self.y))
		r = int(self.r * vista.scale)
		pygame.draw.circle(vista.screen, self.color, screenpos, r)

class Corpse(object):
	lifetime = 3
	def __init__(self, who):
		self.who = who
		self.t = 0
		self.angle = who.angle
		self.omega = random.choice([-1, 1]) * 200
		self.alive = True

	def think(self, dt):
		self.t += dt
		self.x, self.y = self.who.x, self.who.y
		self.angle += dt * self.omega
		if random.random() * 0.1 < dt:
			v = random.uniform(-3, 3), random.uniform(-3, 3)
			state.state.effects.append(Explosion(self, v))
		self.alive = self.t < self.lifetime
		if not self.alive:
			state.state.effects.remove(self)
	
	def draw(self):
		if not self.alive:
			return
		scale = 1 + 2 * self.t / self.lifetime
		alpha = 1 - self.t / self.lifetime
		img.worlddraw(self.who.imgname, (self.x, self.y), self.angle, scale = scale, alpha = alpha)
		



