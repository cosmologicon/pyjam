from __future__ import division, print_function
import random, math, os, pygame
from . import view, pview, state, thing, mist, challenge, settings, hill, sound, endless

class self:
	pass

def init():
	self.t = 0
	self.tlose = 0
	self.sequence = [
		"dialogue A barrier lies in the hills,\nwhich I have never crossed", "", "hopper0", "tier3", "tier3", "save-0",
		"dialogue But today I will cross it.\nToday is different.", "forward", "save-1",
		"dialogue Now I see things from\na new perspective.", "fallback", "save-2",
		"dialogue What lies in front....\nWhat lies behind....", "longjump3", "save-3",
		"dialogue They're all the same from\nthe right point of view.", "leapoffaith", "leapoffaith", "save-4",
		"firstbranch", "dialogue I can only rely on\nwhat can be seen.", "branch3", "save-5",
		"dialogue Whatever is behind something\nmay not even exist.", "ascend", "save-6",
		"dialogue I will avoid the barrier,\nby placing it behind something!", "arcade", "save-7",
		"dialogue I've reached the barrier.\nNow is my chance.", "wall", "save-99",
		"dialogue The only question left is:\nhow far will I run?", "save-end",
	]

	state.reset()
	view.reset()
	state.you = thing.You(x = -settings.lag, y = 0, z = 0)
	state.addhill(thing.Hill(x = 0, y = 0, z = 0, spec = [
		((-40, 0), (10, 0)),
		((-40, -30), (10, -30)),
	]))

	mist.init()

	if os.path.exists(settings.savename):
		lastsave = open(settings.savename, "r").read().strip()
		del self.sequence[:self.sequence.index(lastsave)+1]
	self.nextsaveX0 = None
	resetprofile()
	addchallenge()
	sound.playmusic("call")
	self.taccum = 0

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
	dt *= settings.playspeed
	self.t += dt
	state.you.control(kdowns, kpressed)
	self.taccum += dt
	dtaccum = 1 / settings.ups
	while self.taccum >= 0.5 * dtaccum:
		self.taccum -= dtaccum
		state.think(dtaccum, kdowns, kpressed)
		state.resolve()
	while self.sequence and view.X0 > self.nextaddX0:
		addchallenge()
	while self.nextsaveX0 is not None and view.X0 > self.nextsaveX0:
		self.nextsaveX0 = None
		open(settings.savename, "w").write(self.nextsavename)
		if "end" in self.nextsavename:
			os.remove(settings.savename)
			endless.unlock()
	if state.losing():
		self.tlose += dt
	if self.tlose >= 1 or pygame.K_ESCAPE in kdowns:
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

