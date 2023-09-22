import pygame, math
from . import pview, ptext, quest, state, graphics, progress
from .pview import T

class self:
	pass

def init():
	state.hp = progress.getmaxhp()
	if state.homeconvo is None:
		self.convo = []
	else:
		self.convo = list(convos[state.homeconvo])
		state.homeconvo = None
	self.t = 0
	self.tconvo = 0
	self.buttons = [
		("engine", pygame.Rect(900, 100, 300, 90)),
		("gravnet", pygame.Rect(900, 200, 300, 90)),
		("drag", pygame.Rect(900, 300, 300, 90)),
		("leave", pygame.Rect(640 - 150, 600, 300, 90)),
	]

def think(dt, kdowns = [], kpressed = [0] * 128, mpos = (0, 0), mdowns = set()):
	self.t += dt
	if self.convo:
		self.tconvo += dt
		if self.tconvo > 0.5 and 1 in mdowns:
			del self.convo[0]
	quest.think(dt)

	if 1 in mdowns:
		for bname, rect in self.buttons:
			visible, active, text = bstate(bname)
			if visible and T(rect).collidepoint(mpos):
				if active:
					onclick(bname)
				else:
					pass


def bstate(bname):
	if bname in ("engine", "gravnet"):
		techname = bname.title()
		if state.techlevel[bname] <= 0:
			return False, False, ""
		if state.techlevel[bname] == len(progress.cost[bname]) + 1:
			return True, False, f"Upgrade {techname}\nMAX"
		cost = progress.getcost(bname)
		return True, (cost <= state.xp), f"Upgrade {techname}\n{cost} XP"
	if bname == "drag":
		if state.techlevel[bname] == -1:
			return False, False, ""
		percent = 25 * state.techlevel["drag"]
		return True, True, f"Drag:\n{percent}%"
	if bname == "leave":
		return not self.convo, not self.convo, "Leave"
	
def onclick(bname):
	if bname in ("drag", "engine", "gravnet"):
		progress.upgrade(bname)
	if bname == "leave":
		from . import scene, playscene
		scene.current = playscene
		playscene.resume()
		

def draw():
	pview.fill((60, 60, 60))
	graphics.drawcreature(6, self.t, T(pygame.Rect(100, 100, 500, 500)), pygame.Rect(8, 0, 16, 16))

	if self.convo:
		text = self.convo[0]
		y = math.mix(705, 710, math.cycle(0.2 * self.t))
		ptext.draw(text, midbottom = T(640, y), fontsize = T(50), width = T(1000),
			owidth = 0.5, shadow = (1, 1), shade = 1)
	
	for bname, rect in self.buttons:
		visible, active, text = bstate(bname)
		if visible:
			color = (255, 255, 255) if active else (50, 50, 50)
			pygame.draw.rect(pview.screen, (100, 100, 200), T(rect), T(4))
			ptext.draw(text, center = T(rect.center), fontsize = T(40),
				color = color, owidth = 0.5)

convos = {
	0: [
		"So, you want to hunt unmatter, huh? Well you came to the right place, heh heh. This sector is loaded with it.",
		"We've equipped your ship with a gravnet system. Fire a gravnet at some unmatter so we can track it.",
		"Unfortunately no instruments can detect unmatter until you've got it in a net. You'll just have to look very closely for what isn't there.",
	],
	1: [
		"Fly around in the area around this station and look closely.",
		"The unmatter will appear as black objects blocking out the background stars and nebula.",
		"If you're having trouble seeing anything, check out the README for instructions of how to adjust the brightness.",
		"It should be challenging but not frustrating.",
	],
	2: [
		"That's some good data, mmm, keep it coming!",
		"The more unmatter you find, the more tech we can access, not to mention upgrades to your ship.",
		"We can now measure how many pieces of unmatter are still orbiting this station.",
		"Locating them, though, that's still on you.",
	],
	3: [
		"Strange, the counter is changing even when you're not finding anything.",
		"It's possible the unmatter moves from place to place.",
		"If you can get the counter down to 4, that should give us enough data to form a conclusion.",
	],
	4: [
		"We've determined that the unmatter orbits around nexus points in space.",
		"This station is at a nexus point, but there are others out there.",
		"It looks like sometimes unmatter travels between nexus points.",
		"Follow a piece of unmatter that you've found and keep your eye out for more unmatter. You may find another nexus.",
		"Once you find 3 pieces of unmatter around a nexus, we can drop a counter there.",
	],
}


