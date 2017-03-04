import random, math
from . import state, thing, progress, mechanics, sound

def reset(self):
	self.lastshot = self.t
	self.lastangle = random.angle()

def fullreset(self):
	reset(self)
	self.lastclick = None

def think(self, dt):
	flavors = self.flavors()
	if flavors not in progress.learned:
		return
	if self.disabled:
		self.disabled = max(0, self.disabled - dt)
	else:
		eval("think" + flavors)(self, dt)

def onclick(self):
	flavors = self.flavors()
	if flavors not in progress.learned:
		return
	if flavors == "XYZ":
		if self.lastclick is not None and self.t - self.lastclick < mechanics.tdoubleclick:
			self.die()
			thing.Shockwave(x = self.x, y = self.y, dhp = mechanics.XYZstrength, wavesize = mechanics.XYZwavesize).addtostate()
			sound.playsfx("boom")
		else:
			self.lastclick = self.t
	if flavors == "ZZZ":
		if self.lastclick is not None and self.t - self.lastclick < mechanics.tdoubleclick:
			self.die()
			thing.Shockwave(x = self.x, y = self.y, dhp = mechanics.ZZZstrength, wavesize = mechanics.ZZZwavesize).addtostate()
			sound.playsfx("boom")
		else:
			self.lastclick = self.t

def qfrontmost(obj):
	return -state.cell.distanceto((obj.x, obj.y))

def qstrongest(obj):
	return obj in state.bosses, obj.hp

def qweakest(obj):
	return -obj.hp

def thinkX(self, dt):
	trytoshoot(self, tshot = mechanics.Xrecharge, shotrange = mechanics.Xrange, dhp = mechanics.Xstrength, rewardprob = mechanics.Xrewardprob, kick = mechanics.Xkick, quality = qfrontmost)

def thinkXX(self, dt):
	trytoshoot(self, tshot = mechanics.XXrecharge, shotrange = mechanics.XXrange, dhp = mechanics.XXstrength, rewardprob = mechanics.XXrewardprob,
		kick = mechanics.XXkick, quality = qstrongest)

def thinkXY(self, dt):
	trytoshoot(self, tshot = mechanics.XYrecharge, shotrange = mechanics.XYrange, dhp = mechanics.XYstrength, rewardprob = mechanics.XYrewardprob, kick = mechanics.XYkick, quality = qfrontmost)
	spawnATP(self, atype = thing.ATP1, recharge = mechanics.XYatprecharge, kick = mechanics.XYatpkick)

def thinkXXX(self, dt):
	trytoshoot(self, tshot = mechanics.XXXrecharge, shotrange = mechanics.XXXrange, dhp = mechanics.XXXstrength, rewardprob = mechanics.XXXrewardprob, kick = mechanics.XXXkick, quality = qweakest)

def thinkXXY(self, dt):
	trytoshoot(self, tshot = mechanics.XXYrecharge, shotrange = mechanics.XXYrange, dhp = mechanics.XXYstrength, rewardprob = mechanics.XXYrewardprob, kick = mechanics.XXYkick, quality = qfrontmost)

def thinkXYY(self, dt):
	trytoshoot(self, tshot = mechanics.XYYrecharge, shotrange = mechanics.XYYrange, dhp = mechanics.XYYstrength, rewardprob = mechanics.XYYrewardprob, kick = mechanics.XYYkick, quality = qstrongest)

def thinkXZ(self, dt):
	trytoshootexploding(self, tshot = mechanics.XZrecharge, shotrange = mechanics.XZrange, dhp = mechanics.XZstrength,
		shockdhp = mechanics.XZaoestrength, rewardprob = mechanics.XZrewardprob, shockkick = mechanics.XZkick, wavesize = mechanics.XZaoesize)

def thinkXXZ(self, dt):
	trytoshootexploding(self, tshot = mechanics.XXZrecharge, shotrange = mechanics.XXZrange, dhp = mechanics.XXZstrength,
		shockdhp = mechanics.XXZaoestrength, rewardprob = mechanics.XXZrewardprob, shockkick = mechanics.XXZkick, wavesize = mechanics.XXZaoesize,
		quality = qstrongest)

def thinkY(self, dt):
	spawnATP(self, atype = thing.ATP1, recharge = mechanics.Yrecharge, kick = mechanics.Ykick)

def thinkYYY(self, dt):
	spawnATP(self, atype = thing.ATP2, recharge = mechanics.YYYrecharge, kick = mechanics.YYYkick)

def thinkYZ(self, dt):
	spawnATP(self, atype = thing.ATP2, recharge = mechanics.YZrecharge, kick = mechanics.YZkick)

def thinkXYZ(self, dt):
	pass

def thinkZZZ(self, dt):
	pass

def thinkZ(self, dt):
	trytoheal(self, tshot = mechanics.Zrecharge, shotrange = mechanics.Zrange, dheal = mechanics.Zstrength)

def thinkYZZ(self, dt):
	trytoheal(self, tshot = mechanics.YZZrecharge, shotrange = mechanics.YZZrange, dheal = mechanics.YZZstrength)

def thinkZZ(self, dt):
	trytolaser(self, tshot = mechanics.ZZrecharge, shotrange = mechanics.ZZrange, dhp = mechanics.ZZstrength, quality = qstrongest)

def thinkXZZ(self, dt):
	trytolaser(self, tshot = mechanics.XZZrecharge, shotrange = mechanics.XZZrange, dhp = mechanics.XZZstrength, quality = qstrongest)

def thinkYY(self, dt):
	for obj in state.mouseables:
		if isinstance(obj, (thing.ATP1, thing.ATP2)) and obj.t > 1 and self.distanceto((obj.x, obj.y)) < mechanics.YYrange:
			obj.onhover()
			obj.target = self

def thinkYYZ(self, dt):
	for obj in state.mouseables:
		if isinstance(obj, (thing.ATP1, thing.ATP2)) and obj.t > 1 and self.distanceto((obj.x, obj.y)) < mechanics.YYZrange:
			obj.onhover()
			obj.target = self


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

def gettarget(self, objs, rmax, quality = None):
	canhit = [obj for obj in objs if (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 < (rmax + obj.rcollide) ** 2]
	if not canhit:
		return None
	if quality:
		return max(canhit, key = quality)
	else:
		return min(canhit, key = lambda obj: math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) - obj.rcollide)

def trytoshoot(self, tshot, shotrange, dhp, rewardprob, kick, quality = None):
	if self.lastshot + tshot < self.t:
		toshoot = gettarget(self, state.shootables, shotrange, quality = quality)
		if toshoot:
			thing.Bullet(self, target = toshoot, x = self.x, y = self.y,
				dhp = dhp, rewardprob = rewardprob, kick = kick).addtostate()
			self.lastshot = self.t
			sound.playsfx("laser")

def trytoshootexploding(self, tshot, shotrange, dhp, shockdhp, rewardprob, shockkick, wavesize, quality = None):
	if self.lastshot + tshot < self.t:
		toshoot = gettarget(self, state.shootables, shotrange, quality = quality)
		if toshoot:
			thing.ExplodingBullet(self, target = toshoot, x = self.x, y = self.y,
				dhp = dhp, shockdhp = shockdhp, rewardprob = rewardprob, shockkick = shockkick,
				wavesize = wavesize).addtostate()
			self.lastshot = self.t
			sound.playsfx("laser")

def trytolaser(self, tshot, shotrange, dhp, quality = None):
	if self.lastshot + tshot < self.t:
		toshoot = gettarget(self, state.shootables, shotrange, quality = quality)
		if toshoot:
			thing.Laser(self, toshoot, color = (255, 255, 128)).addtostate()
			toshoot.shoot(dhp)
			self.lastshot = self.t

def trytoheal(self, tshot, shotrange, dheal):
	if self.lastshot + tshot < self.t:
		toshoot = gettarget(self, [obj for obj in state.buildables if obj.disabled], shotrange,
			quality = lambda obj: obj.disabled)
		if toshoot:
			thing.HealRay(self, target = toshoot, x = self.x, y = self.y,
				dheal = dheal).addtostate()
			self.lastshot = self.t

def getcolor(self):
	flavors = "".join(sorted("XYZ"[obj.flavor] for obj in self.slots))
	if self.disabled:
		return int(100 + 80 * math.sin(10 * self.disabled)), 0, 0
	if flavors not in progress.learned:
		return 30, 30, 30
	if flavors in ("X", "XX", "XY", "XXX", "XXY", "XYY"):
		return 150, 0, 200
	if flavors in ("XZ", "XXZ"):
		return 200, 0, 150
	if flavors in ("ZZ", "XZZ"):
		return 200, 200, 0
	if flavors in ("Y", "YYY", "YZ"):
		return 50, 200, 50
	if flavors in ("XYZ", "ZZZ"):
		return 50, 50, 255

	return 0, 200, 200


