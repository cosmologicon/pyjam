from __future__ import division, print_function
import os, random, math, pygame
from . import settings, view, state, thing, mist, challenge, sound, hill, pview, ptext
from .pview import T

def currentscore():
	return view.X0 * 0.02 + self.score0
def isunlocked():
	return os.path.exists(settings.scorename)
def unlock():
	if isunlocked():
		return
	open(settings.scorename, "w").write("0")
def gethiscore():
	if not isunlocked():
		return None
	return int(open(settings.scorename, "r").read().strip())
def savescore():
	hiscore = gethiscore()
	if hiscore is None or currentscore() > hiscore:
		open(settings.scorename, "w").write(str(int(currentscore())))

def colormix(x, y, a):
	return tuple(int(math.clamp(math.mix(p, q, a), 0, 255)) for p, q in zip(x, y))


class self:
	pass

def getspeed():
	x = currentscore() / 200
	return 1 + 1.2 * (1 - math.exp(-x))

skycolors = {
	0: (100, 100, 255),
	1: (255, 150, 100),
	2: (180, 180, 220),
	3: (150, 255, 100),
}

hillcolors = {
	0: [(180, 100, 40), (40, 100, 40)],
	1: [(180, 180, 20), (160, 120, 40)],
	2: [(80, 80, 80), (30, 30, 30)],
	3: [(120, 160, 255), (200, 200, 255)],
}

def getscene():
	nscene = len(skycolors)
	scenelength = 40
	dlength = 4
	score = currentscore()
	jscene = int(score / scenelength) % nscene
	lastscene = (jscene - 1) % nscene if score > scenelength else 0
	f = math.clamp(score % scenelength / dlength, 0, 1)
	return lastscene, jscene, f

def init():
	self.t = 0
	self.tlose = 0
	self.score0 = 0.5 * (gethiscore() or 0)

	state.reset()
	view.reset()
	state.you = thing.You(x = -settings.lag, y = 0, z = 0)
	state.addhill(thing.Hill(x = 0, y = 0, z = 0, spec = [
		((-40, 0), (10, 0)),
		((-40, -30), (10, -30)),
	]))
	mist.init()

	self.lastchallenges = []
	addchallenge()
	sound.playmusic("party")
	self.taccum = 0

def resetprofile():
	self.profile = {}
def startprofile(name):
	self.profile[name] = pygame.time.get_ticks()
def stopprofile(name):
	self.profile[name] = pygame.time.get_ticks() - self.profile[name]

def getchallenge():
	challenges = ["hopper0", "tier3", "arcade", "backunder", "leapoffaith", "forward", "fallback"]
	if currentscore() > 40:
		challenges += ["ascend", "longjump3", "hazard3", "shortcliff"]
	if currentscore() > 80:
		challenges += ["longjump3", "hazard3", "tier3"]
	if currentscore() > 120:
		challenges += ["hazard3", "tier3"]
	while True:
		c = random.choice(challenges)
		if c not in self.lastchallenges:
			break
	self.lastchallenges.append(c)
	self.lastchallenges = self.lastchallenges[-3:]
	return c

def addchallenge():
	cname = getchallenge()
	_, s, _ = getscene()
	hillcolor, grasscolor = hillcolors[s]
	challenge.addchallenge(cname, signs = False, hillcolor = hillcolor, grasscolor = grasscolor)
	self.nextaddX0 = state.endingX0at(120)

def think(dt, kdowns, kpressed):
	dt *= getspeed()
	self.t += dt
	state.you.control(kdowns, kpressed)
	self.taccum += dt
	dtaccum = 1 / settings.ups
	while self.taccum >= 0.5 * dtaccum:
		self.taccum -= dtaccum
		state.think(dtaccum, kdowns, kpressed)
		state.resolve()
	while view.X0 > self.nextaddX0:
		addchallenge()
	if state.losing():
		self.tlose += dt
	if self.tlose >= 1 or pygame.K_ESCAPE in kdowns:
		savescore()
		from . import menuscene, scene
		scene.set(menuscene)
	hill.killtime(0.005)

def draw():
	s0, s1, fs = getscene()
	skycolor = colormix(skycolors[s0], skycolors[s1], fs)

	pview.fill(skycolor)
	objs = list(state.hills) + list(state.effects) + list(state.hazards)
	objs.sort(key = lambda obj: (obj.z, -obj.y))
	for obj in objs:
		obj.draw()
	state.you.draw()
	if self.t < 1:
		a = math.clamp(int(255 * (1 - math.smoothfade(self.t, 0, 1))), 0, 255)
		pview.fill((255, 255, 255, a))
	if self.tlose > 0:
		a = math.clamp(int(255 * math.smoothfade(self.tlose, 0, 0.5)), 0, 255)
		pview.fill((255, 255, 255, a))
	ptext.draw("Distance: %d m" % currentscore(), topright = T(1000, 24),
		fontsize = T(30), color = "black",
		fontname = "Acme")


