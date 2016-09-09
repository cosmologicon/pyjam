import random, math
from . import state, thing, progress, mechanics

def reset(self):
	self.lastshot = self.t
	self.lastangle = random.angle()

def fullreset(self):
	reset(self)
	self.lastclick = None

def think(self, dt):
	flavors = "".join(sorted("XYZ"[obj.flavor] for obj in self.slots))
	if flavors not in progress.learned:
		return
	if self.disabled:
		self.disabled = max(0, self.disabled - dt)
	else:
		eval("think" + flavors)(self, dt)

def onclick(self):
	flavors = "".join(sorted("XYZ"[obj.flavor] for obj in self.slots))
	if flavors not in progress.learned:
		return
	if flavors == "XYZ":
		print self.lastclick
		if self.lastclick is not None and self.t - self.lastclick < mechanics.tdoubleclick:
			self.die()
			thing.Shockwave(x = self.x, y = self.y, dhp = mechanics.XYZstrength, wavesize = mechanics.XYZwavesize).addtostate()
		else:
			self.lastclick = self.t
			


def thinkX(self, dt):
	trytoshoot(self, tshot = mechanics.Xrecharge, shotrange = mechanics.Xrange, dhp = mechanics.Xstrength, rewardprob = mechanics.Xrewardprob, kick = mechanics.Xkick)

def thinkXX(self, dt):
	trytoshoot(self, tshot = mechanics.XXrecharge, shotrange = mechanics.XXrange, dhp = mechanics.XXstrength, rewardprob = mechanics.XXrewardprob, kick = mechanics.XXkick)

def thinkXY(self, dt):
	trytoshoot(self, tshot = mechanics.XYrecharge, shotrange = mechanics.XYrange, dhp = mechanics.XYstrength, rewardprob = mechanics.XYrewardprob, kick = mechanics.XYkick)

def thinkXXX(self, dt):
	trytoshoot(self, tshot = mechanics.XXXrecharge, shotrange = mechanics.XXXrange, dhp = mechanics.XXXstrength, rewardprob = mechanics.XXXrewardprob, kick = mechanics.XXXkick)

def thinkXXY(self, dt):
	trytoshoot(self, tshot = mechanics.XXYrecharge, shotrange = mechanics.XXYrange, dhp = mechanics.XXYstrength, rewardprob = mechanics.XXYrewardprob, kick = mechanics.XXYkick)

def thinkY(self, dt):
	spawnATP(self, atype = thing.ATP1, recharge = mechanics.Yrecharge, kick = mechanics.Ykick)

def thinkYY(self, dt):
	spawnATP(self, atype = thing.ATP2, recharge = mechanics.YYrecharge, kick = mechanics.YYkick)

def thinkYZ(self, dt):
	spawnATP(self, atype = thing.ATP2, recharge = mechanics.YZrecharge, kick = mechanics.YZkick)

def thinkXYZ(self, dt):
	pass

def thinkZ(self, dt):
	trytoheal(self, tshot = mechanics.Zrecharge, shotrange = mechanics.Zrange, dheal = mechanics.Zstrength)


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

def trytoshoot(self, tshot, shotrange, dhp, rewardprob, kick):
	if self.lastshot + tshot < self.t:
		toshoot, r2 = None, shotrange ** 2
		for obj in state.shootables:
			dx = obj.x - self.x
			dy = obj.y - self.y
			if dx ** 2 + dy ** 2 < r2:
				toshoot = obj
				r2 = dx ** 2 + dy ** 2
		if toshoot:
			thing.Bullet(self, target = toshoot, x = self.x, y = self.y,
				dhp = dhp, rewardprob = rewardprob, kick = kick).addtostate()
			self.lastshot = self.t

def trytoheal(self, tshot, shotrange, dheal):
	if self.lastshot + tshot < self.t:
		toshoot, r2 = None, shotrange ** 2
		for obj in state.buildables:
			if not obj.disabled:
				continue
			dx = obj.x - self.x
			dy = obj.y - self.y
			if dx ** 2 + dy ** 2 < r2:
				toshoot = obj
				r2 = dx ** 2 + dy ** 2
		if toshoot:
			thing.HealRay(self, target = toshoot, x = self.x, y = self.y,
				dheal = dheal).addtostate()
			self.lastshot = self.t

def getcolor(self):
	flavors = "".join(sorted("XYZ"[obj.flavor] for obj in self.slots))
	return 200, 100, 0	


