import random, math
from . import state, thing, progress, mechanics

def reset(self):
	self.lastshot = self.t
	self.lastangle = random.angle()

def think(self, dt):
	from . import thing
	flavors = "".join(sorted("XYZ"[obj.flavor] for obj in self.slots))
	if flavors not in progress.learned:
		return
	eval("think" + flavors)(self, dt)


def thinkX(self, dt):
	trytoshoot(self, tshot = mechanics.Xrecharge, shotrange = mechanics.Xrange, dhp = mechanics.Xstrength, rewardprob = mechanics.Xrewardprob)

def thinkXX(self, dt):
	trytoshoot(self, tshot = mechanics.XXrecharge, shotrange = mechanics.XXrange, dhp = mechanics.XXstrength, rewardprob = mechanics.XXrewardprob)

def thinkXY(self, dt):
	trytoshoot(self, tshot = mechanics.XYrecharge, shotrange = mechanics.XYrange, dhp = mechanics.XYstrength, rewardprob = mechanics.XYrewardprob)

def thinkXXX(self, dt):
	trytoshoot(self, tshot = mechanics.XXXrecharge, shotrange = mechanics.XXXrange, dhp = mechanics.XXXstrength, rewardprob = mechanics.XXXrewardprob)

def thinkXXY(self, dt):
	trytoshoot(self, tshot = mechanics.XXYrecharge, shotrange = mechanics.XXYrange, dhp = mechanics.XXYstrength, rewardprob = mechanics.XXYrewardprob)

def thinkY(self, dt):
	spawnATP(self, atype = thing.ATP1, recharge = mechanics.Yrecharge, kick = mechanics.Ykick)

def thinkYY(self, dt):
	spawnATP(self, atype = thing.ATP2, recharge = mechanics.YYrecharge, kick = mechanics.YYkick)

def thinkYZ(self, dt):
	spawnATP(self, atype = thing.ATP2, recharge = mechanics.YZrecharge, kick = mechanics.YZkick)



def spawnATP(self, atype, recharge, kick):
	if self.lastshot + recharge < self.t:
		self.lastangle += (math.sqrt(5) - 1) / 2 * math.tau
		dx = math.sin(self.lastangle)
		dy = math.cos(self.lastangle)
		atp = atype(x = self.x + 6 * dx, y = self.y + 6 * dy)
		r = random.uniform(1, 2) * kick
		atp.kick(r * dx, r * dy)
		atp.addtostate()
		self.lastshot = self.t

def trytoshoot(self, tshot, shotrange, dhp, rewardprob):
	if self.lastshot + tshot < self.t:
		for obj in state.shootables:
			dx = obj.x - self.x
			dy = obj.y - self.y
			if dx ** 2 + dy ** 2 < shotrange ** 2:
				obj.shoot(dhp, rewardprob)
				thing.Laser(self, obj).addtostate()
				self.lastshot = self.t
				break


