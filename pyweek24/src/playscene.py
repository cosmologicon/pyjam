import random, math, os.path, pygame
from . import view, pview, state, thing, mist, challenge, settings, hill

class self:
	pass

def init():
	self.t = 0
	self.tlose = 0
	self.sequence = [
		"rolling", "hopper0", "save-0",
		"rolling", "forward", "fallback", "save-1",
		"longjump3", "save-2",
		"leapoffaith", "arcade", "save-3",
	]

	state.reset()
	view.reset()
	state.you = thing.You(x = -settings.lag, y = 0, z = 0)
	state.addhill(thing.Hill(x = 0, y = 0, z = 0, spec = [
		((-40, 0), (10, 0)),
		((-40, -30), (10, -30)),
	]))

	mist.init()

	state.effects.append(thing.Sign(text = settings.gamename,
		x = 120, y = -20, z = -25, fontsize = 15, color = "orange", shadow = (1, 1),
		angle = 10))
	state.effects.append(thing.Sign(text = "by Christopher Night",
		x = 200, y = -20, z = -18, fontsize = 5, color = "orange", shadow = (1, 1),
		angle = 10))

	if os.path.exists(settings.savename):
		lastsave = open(settings.savename, "r").read().strip()
		del self.sequence[:self.sequence.index(lastsave)+1]
	self.nextsaveX0 = None
	resetprofile()
	addchallenge()

def resetprofile():
	self.profile = {}
def startprofile(name):
	self.profile[name] = pygame.time.get_ticks()
def stopprofile(name):
	self.profile[name] = pygame.time.get_ticks() - self.profile[name]

def addchallenge():
	startprofile("addchallenge")
	if not self.sequence:
		return
	cname = self.sequence.pop(0)
	if cname.startswith("save-"):
		self.nextsaveX0 = state.endingX0at(-45)
		self.nextsavename = cname
	else:
		challenge.addchallenge(cname)
		self.nextaddX0 = state.endingX0at(90)
	stopprofile("addchallenge")

def think(dt, kdowns, kpressed):
	resetprofile()
	startprofile("think")
	self.t += dt
	state.you.control(kdowns, kpressed)
	state.think(dt, kdowns, kpressed)
	state.resolve()
	while self.sequence and view.X0 > self.nextaddX0:
		addchallenge()
	while self.nextsaveX0 is not None and view.X0 > self.nextsaveX0:
		self.nextsaveX0 = None
		open(settings.savename, "w").write(self.nextsavename)
	if state.losing():
		self.tlose += dt
	if self.tlose >= 1:
		from . import menuscene, scene
		scene.set(menuscene)
	startprofile("hills")
	hill.killtime(0.005)
	stopprofile("hills")
	self.printprofile = settings.DEBUG and kpressed[pygame.K_F2]
	stopprofile("think")

def draw():
	startprofile("draw")
	pview.fill((100, 100, 255))
#	objs = list(state.boards.values()) + list(state.blocks) + list(state.effects) + list(state.hazards)
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
	stopprofile("draw")
	if self.printprofile:
		print(" ".join("%s=%d" % item for item in sorted(self.profile.items())))

