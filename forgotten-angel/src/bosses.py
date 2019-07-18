from __future__ import division
import math, pygame, random
from . import ships, state, vista, sound, effects


class Boss(ships.Ship):
	fadeable = False
	radius = 3
	
	def __init__(self, pos):
		ships.Ship.__init__(self, pos)
		self.corpse = effects.Corpse(self)
		self.hp = self.maxhp

	def die(self):
		ships.Ship.die(self)
		state.state.effects.append(self.corpse)
		sound.play("bossdie")

class Boss1(Boss):
	maxhp = 20
	imgname = "boss1"
	shoottime = 1
	a = 10
	vmax = 2
	
	def __init__(self, pos):
		Boss.__init__(self, pos)
		self.pos0 = pos
		self.t = 0
		self.tmove = 0
		self.laserable = True
		self.zeta = 0

	def think(self, dt):
		self.t += dt
		while self.t > self.shoottime:
			self.t -= self.shoottime
			self.zeta += math.tau / 1.618
			self.launchslug(6, self.zeta)
			self.launchslug(6, self.zeta + math.tau / 3)
			self.launchslug(6, self.zeta + 2 * math.tau / 3)
			sound.play("shoot")
		if self.target is None or math.sqrt((self.x - self.target[0]) ** 2 + (self.y - self.target[1]) ** 2) < 1:
			self.pickrandomtarget(self.pos0, 6)
		Boss.think(self, dt)

"""
class Boss2(Boss):
	maxhp = 10
	imgname = "boss2"
	def __init__(self, pos):
		Boss.__init__(self, pos)
		self.t = 0
		self.tmove = 0
		self.laserable = True

	def think(self, dt):
		self.t += dt
		self.movetime = 5 if self.hp < 6 else 10
		self.vmax = 3 if self.hp < 6 else 1.5
		if self.target is None:
			self.tmove += dt
			if self.tmove > self.movetime:
				for j in range(12):
					self.launchslug(6, j * math.tau / 12)
					self.launchslug(4, (j + 0.5) * math.tau / 12)
				self.pickrandomtarget(self.pos0)
				self.tmove = 0
		self.imgname = "boss1" if self.target or self.tmove + 2 < self.movetime else "red"
		Boss.think(self, dt)
#		self.laserable = not any(escort.hp > 0 for escort in self.escorts)
"""	


class Boss2Escort(ships.Ship):
	fadeable = False
	laserable = True
	imgname = "escort"
	radius = 1
	damage = 2
	def __init__(self, boss, r, theta0, omega):
		self.boss = boss
		self.r = r
		self.theta0, self.omega = theta0, omega
		pos = boss.x, boss.y
		ships.Ship.__init__(self, pos)

	def draw(self):
		if not vista.isvisible((self.x, self.y), self.radius):
			return
		pos = vista.worldtoscreen((self.x, self.y))
		r = int(vista.scale * random.uniform(0.1, 0.4))
		c = random.randint(0, 255)
		pygame.draw.circle(vista.screen, (c, c, 255), pos, r)
		
	def think(self, dt):
		theta = self.theta0 + self.boss.t * self.omega
		r = self.r * self.boss.rfac
		self.x = self.boss.x + r * math.sin(theta)
		self.y = self.boss.y + r * math.cos(theta)
		if self.hp <= 0:
			self.die()
		elif self.distfromyou() < 0.4:
			self.hp = 0
			self.die()
			state.state.you.takedamage(self.damage)

class Boss2(Boss):
	fadeable = False
	imgname = "boss2"
	maxhp = 10
	radius = 10
	def __init__(self, pos):
		Boss.__init__(self, pos)
		self.escorts = [
			Boss2Escort(self, 4, j * math.tau / 6, 2) for j in range(6)
		] + [
			Boss2Escort(self, 6, j * math.tau / 12, -1) for j in range(12)
		]
		state.state.ships.extend(self.escorts)
		self.t = 0
		self.tslug = 0
		self.rfac = 1
		self.laserable = False

	def think(self, dt):
		self.t += dt
		self.rfac = 0.9 + 0.3 * math.sin(self.t)
		self.tslug += dt
		while self.tslug > 1:
			self.tslug -= 1
			self.launchslug(6, 0)
		self.pickrandomtarget(self.pos0)
		ships.Ship.think(self, dt)
		self.laserable = not any(escort.hp > 0 for escort in self.escorts)

	def draw(self):
		if not vista.isvisible((self.x, self.y), self.radius):
			return
		for escort in self.escorts:
			if escort.hp > 0:
				vista.drawbolt((self.x, self.y), (escort.x, escort.y), (100, 100, 255))
		ships.Ship.draw(self)
	
	def takedamage(self, damage):
		if any(escort.hp > 0 for escort in self.escorts):
			return
		ships.Ship.takedamage(self, damage)



