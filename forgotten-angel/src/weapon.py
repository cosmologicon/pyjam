import math
import state, effects, sound

class Weapon(object):
	cooldown = 1
	reach = 4
	damage = 1
	soundname = None
	
	def __init__(self, parent):
		self.parent = parent
		self.tcool = 0

	def canfire(self):
		return self.tcool <= 0

	def canreach(self, obj):
		dx, dy = self.parent.x - obj.x, self.parent.y - obj.y
		return dx ** 2 + dy ** 2 < self.reach ** 2

	def think(self, dt):
		self.tcool = max(self.tcool - dt, 0)

	def fire(self, target):
		self.tcool = self.cooldown
		if self.soundname:
			sound.play(self.soundname)

class Laser(Weapon):
	reach = 4
	color = 255, 0, 0
	soundname = "laser"
	cooldown = 5

	def fire(self, target):
		Weapon.fire(self, target)
		target.takedamage(self.damage)
		state.state.effects.append(effects.Laser(self.parent, target, self.color))

class Gun(Weapon):
	reach = 8
	damage = 5
	soundname = "shot"

	def fire(self, target):
		Weapon.fire(self, target)
		state.state.effects.append(effects.Bullet(self.parent, target, self.damage))	

	def canreach(self, obj):
		dx, dy = obj.x - self.parent.x, obj.y - self.parent.y
		d = math.sqrt(dx ** 2 + dy ** 2)
		if d > self.reach:
			return False
		vx, vy = self.parent.vx, self.parent.vy
		v = math.sqrt(vx ** 2 + vy ** 2)
		return dx * vx + dy * vy > 0.9 * d * v

class YouLaser(Laser):
	reach = 6
	color = 255, 255, 0
	cooldown = 1

class YouDrill(Laser):
	reach = 1
	color = 255, 255, 255
	soundname = "drill"
	damage = 10
	cooldown = 0.1

	def fire(self, target):
		Weapon.fire(self, target)
		target.takedamage(self.damage)


# The weapon for things that explode when they hit something.
class Trigger(Weapon):
	reach = 0.4
	damage = 1
	cooldown = 0
	soundname = "boom"

	def fire(self, target):
		Weapon.fire(self, target)
		target.takedamage(self.damage)
		self.parent.die()



