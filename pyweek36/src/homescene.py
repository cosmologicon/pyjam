import pygame, math
from . import pview, ptext, quest, state, graphics, progress, hud, view, settings
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
	cols = [
		["engine", "gravnet", "health", "energy", None, "drag", "leave"],
		["beam", "ring", "glow", None, "map", "drive", "return"],
	]
	self.buttons = [
		(bname, pygame.Rect(700 + 300 * x, 100 + 80 * y, 270, 70))
		for x, col in enumerate(cols) for y, bname in enumerate(col) if bname is not None
	]

def think(dt, kdowns = [], kpressed = [0] * 128, mpos = (0, 0), mdowns = set()):
	self.t += dt
	if self.convo:
		self.tconvo += dt
		if self.tconvo > 0.5 and 1 in mdowns:
			del self.convo[0]
	elif 1 in mdowns:
		for bname, rect in self.buttons:
			visible, active, text = bstate(bname)
			if visible and T(rect).collidepoint(mpos):
				if active:
					onclick(bname)
				else:
					pass
	quest.think(dt)



def bstate(bname):
	if bname in ("engine", "gravnet", "health", "energy", "beam", "ring", "glow"):
		techname = bname.upper()
		if state.techlevel[bname] < 0:
			return False, False, ""
		if state.techlevel[bname] == len(progress.cost[bname]):
			return True, False, f"{techname}\nMAX LEVEL"
		cost = progress.getcost(bname)
		if cost is None:
			return False, False, ""
		else:
			return True, (cost <= state.xp), f"UPGRADE {techname}\n{cost} XP"
	if bname in ("map", "drive", "return"):
		techname = bname.upper()
		if state.techlevel[bname] == 1:
			return True, False, f"{techname}\nUNLOCKED"
		elif state.techlevel[bname] == 0:
			cost = progress.getcost(bname)
			return True, (cost <= state.xp), f"UNLOCK {techname}\n{cost} XP"
	if bname == "drag":
		if state.techlevel[bname] == -1:
			return False, False, ""
		percent = 25 * state.techlevel["drag"]
		return True, True, f"DRAG: {percent}%"
	if bname == "leave":
		return not self.convo, not self.convo, "LEAVE"
	
def onclick(bname):
	if bname in ("drag", "engine", "gravnet", "health", "energy", "beam", "ring", "glow", "map", "drive", "return"):
		progress.upgrade(bname)
	if bname == "leave":
		from . import scene, playscene
		scene.current = playscene
		playscene.resume()
		

def draw():
	pview.fill((0, 0, 0))
	view.xG0 = self.t * 0.5
	settings.nebula += 5
	settings.stars += 5
	graphics.drawnebula()
	graphics.drawstars()
	settings.nebula -= 5
	settings.stars -= 5
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
		ptext.draw("CLICK TO CONTINUE", midbottom = T(960, 710), fontsize = T(18), shade = 1)
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
				rect = rect.inflate(-T(8), -T(8))
				ptext.drawbox(text, T(rect), color = bcolor, owidth = 0.5)
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
		"If it's too subtle and you're having trouble seeing anything, press F9 to adjust the brightness.",
		"It should be challenging but not frustrating.",
	],
	2: [
		"That's some good data, mmm, keep it coming!",
		"The more unmatter you find, the more tech we can access, not to mention upgrades to your ship.",
		"We can now measure how many pieces of unmatter are still orbiting this station.",
		"Locating them, though, that's still on you.",
	],
	3: [
		"Strange, the counter is changing even while you're not finding anything.",
		"It's possible the unmatter moves from place to place.",
		"If you can get the counter down to 4, that should give us enough data to form a conclusion.",
	],
	4: [
		"We've determined that the unmatter orbits around nexus points in space.",
		"This station is at a nexus point, but there are others out there.",
		"It looks like sometimes unmatter travels between nexus points.",
		"Follow a piece of unmatter that you've found and keep your eye out for more unmatter along the way. If you find a cluster of them, it must be another nexus.",
		"Once you find 3 pieces of unmatter around a nexus, we can drop a counter there.",
	],
	"beam": [
		"Behold! I call it the Xazer beam. This will definitely let you pick out unmatter more easily.",
		"You've got a limited number of uses, but come back here any time to recharge.",
		"Once you turn it on it will last until you fire a gravnet.",
	],
	"ring": [
		"Get out there and find more nexus points!",
		"3 pieces of unmatter around a nexus point lets us deploy a counter.",
	],
	"ring": [
		"Behold, the Xazer Ring.",
	],
	"glow": [
		"Again, this lasts until you fire a gravnet.",
	],
	"drive": [
		"This hyperdrive should let you reach outer areas much faster.",
		"It will last until you fire a gravnet, and you'll be invulnerable while using it.",
		"I recommend saving one charge to get back, though!",
	],
}


