import random, math
from . import state, thing

def reset(self):
	self.lastshot = self.t
	self.lastangle = random.angle()

def think(self, dt):
	from . import thing
	flavors = "".join(map(str, sorted(obj.flavor for obj in self.slots)))
	if flavors == "0":
		think0(self, dt)
	if flavors == "1":
		think1(self, dt)


def think0(self, dt):
	trytoshoot(self, tshot = 2, shotrange = 30, dhp = 1)

def think1(self, dt):
	if self.lastshot + 2 < self.t:
		self.lastangle += (math.sqrt(5) - 1) / 2 * math.tau
		dx = math.sin(self.lastangle)
		dy = math.cos(self.lastangle)
		atp = thing.ATP(x = self.x + 6 * dx, y = self.y + 6 * dy)
		r = random.uniform(40, 80)
		atp.kick(r * dx, r * dy)
		atp.addtostate()
		self.lastshot = self.t

def trytoshoot(self, tshot, shotrange, dhp):
	if self.lastshot + tshot < self.t:
		for obj in state.shootables:
			dx = obj.x - self.x
			dy = obj.y - self.y
			if dx ** 2 + dy ** 2 < shotrange ** 2:
				obj.shoot(dhp)
				thing.Laser(self, obj).addtostate()
				self.lastshot = self.t
				break


