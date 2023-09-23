import pygame, math
from . import pview, ptext, quest, state, graphics, progress, hud
from .pview import T

class self:
	pass

def init():
	state.hp = progress.getmaxhp()
	state.energy = progress.getmaxenergy()
	state.you.onhome()
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
		("leave", pygame.Rect(960 - 100, 630, 200, 50)),
	]

def think(dt, kdowns = [], kpressed = [0] * 128, mpos = (0, 0), mdowns = set()):
	self.t += dt
	if self.convo:
		self.tconvo += dt
		if self.tconvo > 0.5 and 1 in mdowns:
			del self.convo[0]
	quest.think(dt)

	if 1 in mdowns and not self.convo:
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
		if state.techlevel[bname] < 0:
			return False, False, ""
		if state.techlevel[bname] == len(progress.cost[bname]) + 1:
			return True, False, f"Upgrade {techname}\nMAX"
		cost = progress.getcost(bname)
		if cost is None:
			return False, False, ""
		else:
			return True, (cost <= state.xp), f"Upgrade {techname}\n{cost} XP"
	if bname == "drag":
		if state.techlevel[bname] == -1:
			return False, False, ""
		percent = 25 * state.techlevel["drag"]
		return True, True, f"Drag:\n{percent}%"
	if bname == "leave":
		return not self.convo, not self.convo, "LEAVE"
	
def onclick(bname):
	if bname in ("drag", "engine", "gravnet"):
		progress.upgrade(bname)
	if bname == "leave":
		from . import scene, playscene
		scene.current = playscene
		playscene.resume()
		

def draw():
	pview.fill((60, 60, 60))
#	graphics.drawcreature(6, self.t, T(pygame.Rect(100, 100, 500, 500)), pygame.Rect(8, 0, 16, 16))
	graphics.draw("alien", T(380, 360), pview.f * 0.8, 0)
	rect = pygame.Rect(T(0, 0, 580, 580))
	rect.center = T(380, 360)
	color = 60, 180, 180
	pygame.draw.rect(pview.screen, color, rect, T(20), border_radius = T(40))
	rect.inflate_ip(-T(5), -T(5))
	rect.move_ip(-T(2), -T(2))
	color = math.imix(color, (255, 255, 255), 0.1)
	pygame.draw.rect(pview.screen, color, rect, T(5), border_radius = T(40))
	

	if self.convo:
		text = self.convo[0]
		y = math.mix(360, 366, math.cycle(0.2 * self.t))
		ptext.draw(text, center = T(960, y), fontname = "JollyLodger", fontsize = T(70), width = T(540),
			color = "#ff7fff", owidth = 0.5, shadow = (1, 1), shade = 1)
	else:
		for bname, rect in self.buttons:
			visible, active, text = bstate(bname)
			if visible:
				bcolor = (50, 50, 150) if active else (20, 20, 20)
				pygame.draw.rect(pview.screen, bcolor, T(rect), 0, border_radius = T(8))
				bcolor = math.imix(bcolor, (255, 255, 255), 0.05)
				pygame.draw.rect(pview.screen, bcolor, T(rect), T(6), border_radius = T(8))
				if active:
					bcolor = math.imix(bcolor, (255, 255, 255), 0.5)
				ptext.draw(text, center = T(rect.center), fontsize = T(28),
					color = bcolor, owidth = 0.5)
	hud.draw()

convos = {
	0: [
		"So, you want to hunt unmatter, huh? Well you came to the right place, heh heh. This sector is loaded with it.",
		"We've equipped your ship with a gravnet system. Fire a gravnet at some unmatter so we can track it.",
		"Unfortunately no instruments can detect unmatter until you've got it in a net. You'll just have to look very closely for what isn't there.",
	],
	1: [
		"Fly around in the area around this station and look closely.",
		"The unmatter will appear as black objects blocking out the background stars and nebula.",
		"If you're having trouble seeing anything, press F9 to adjust the brightness.",
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
	"beam": [
		"Behold! I call it the Xazer beam. This should really help out.",
		"You've got a limited number of uses, but come back here any time to recharge.",
		"Once you turn it on it will last until you fire a gravnet.",
	],
	"ring": [
	],
	"drive": [
		"This hyperdrive should let you reach outer areas much faster.",
		"It will last until you fire a gravnet, and you'll be invulnerable while using it.",
		"I recommend saving one charge to get back, though!",
	],
}


