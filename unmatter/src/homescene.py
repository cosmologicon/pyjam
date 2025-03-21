import pygame, math
from . import pview, ptext, quest, state, graphics, progress, hud, view, settings, sound
from .pview import T

class self:
	pass

def init():
	pygame.mouse.set_visible(True)
	sound.playmusic("journey-to-ascend", 0.5)
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
		["beam", "ring", "glow", "map", "drive", "return", "ending"],
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
					sound.play("no")
	quest.think(dt)


upgradetechs = {
	"engine": "ENGINE",
	"gravnet": "GRAVNET",
	"health": "HULL STRENGTH",
	"energy": "CHARGE",
	"beam": "XAZER BEAM",
	"ring": "LINZ FLARE",
	"glow": "SEARCHLIGHT",
}
unlocktechs = {
	"map": "SECTOR MAP",
	"drive": "HYPERDRIVE",
	"return": "STATION WARP",
	"ending": "MYSTERY",
}

def bstate(bname):
	if bname in upgradetechs:
		techname = upgradetechs[bname]
		if state.techlevel[bname] < 0:
			return False, False, ""
		if state.techlevel[bname] == len(progress.cost[bname]):
			return True, False, f"{techname}\nMAX LEVEL"
		cost = progress.getcost(bname)
		if cost is None:
			return False, False, ""
		else:
			return True, (cost <= state.xp), f"UPGRADE {techname}\n{cost} XP"
	if bname == "ending":
		techname = unlocktechs[bname]
		if state.techlevel[bname] == 1:
			return True, False, f"{techname}\nUNLOCKED"
		elif state.techlevel[bname] == 0:
			visible = all(state.techlevel[tech] > 0 for tech in ("map", "drive", "return"))
			cost = progress.getcost(bname)
			return visible, (cost <= state.xp), f"UNLOCK {techname}\n{cost} XP"
	elif bname in unlocktechs:
		techname = unlocktechs[bname]
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
	if bname == "ending":
		self.convo = list(convos["ending"])
		progress.upgrade("ending")
		quest.marquee.append("TECH UNLOCKED: REPAIR COUNTERS")
		sound.play("win")
		return
	if bname == "drag":
		progress.upgrade(bname)
		sound.play("click")
	if bname in upgradetechs:
		progress.upgrade(bname)
		sound.play("unlock")
	if bname in unlocktechs:
		self.convo = list(convos[bname])
		quest.marquee.append(f"TECH UNLOCKED: {unlocktechs[bname]}")
		progress.upgrade(bname)
		sound.play("unlock")
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
	graphics.draw("alien", T(380, 372), pview.f * 0.8, 0)
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
			color = "#7fffff", owidth = 0.5, shadow = (1, 1), shade = 1)
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
		"So, you're interested in unmatter, that hot new particle that everyone's talking about, huh?",
		"Well you came to the right place, heh heh. This sector is loaded with it.",
		"We've equipped your ship with a gravitational net launcher. Throw a gravnet at some unmatter so we can track it.",
		"Unfortunately no instruments can detect unmatter until you've got it in a net. You'll just have to look very closely to see what isn't there.",
	],
	1: [
		"There's a bunch of unmatter orbiting the station right now.",
		"Want my advice for finding it? Fly a little bit away from the station and sit still for a minute, and just watch the stars.",
		"Stay within the orange circle on your map, at least for now.",
		"The unmatter will appear as black objects blocking out the background stars and nebula.",
		"If it's too subtle and you're having trouble seeing the nebula, press F9 to adjust the display settings.",
		"This should be challenging but not frustrating.",
	],
	2: [
		"That's some good data you're collecting, mmm, keep it coming!",
		"The more unmatter you find, the more tech we can build, not to mention upgrades to your ship.",
		"We can now measure how many pieces of unmatter are still orbiting this station that we haven't located.",
		"You don't need to get them all, but at least a few more.",
	],
	3: [
		"Strange, the counter does go down when you find a piece of unmatter, but it's also going up and down on its own.",
		"It's possible the unmatter moves from place to place, but we need more data to form a conclusion.",
		"If you can get the station counter down to 4, that should be enough.",
	],
	4: [
		"From what we can tell, the unmatter orbits around gravity wells in space.",
		"This station is at a gravity well, but there are others out there.",
		"It looks like sometimes unmatter travels between gravity wells, so if you see one leaving from the station, you may be able to follow it to another well.",
		"If you find some unmatter in another well, we should be able to deploy a counter there.",
	],
	"beam": [
		"Behold, my latest invention! I call it the Xazer beam, after my brother in law's pet flarg Xazer.",
		"Once my technicians finish duct taping it to your hull, this will let you pick out unmatter more easily.",
		"You've got a limited number of uses, but come back here any time to recharge.",
		"Once activated it will last until you throw a gravnet.",
	],
	"more": [
		"Get out there and find more gravity wells!",
		"3 pieces of unmatter around a well lets us deploy a counter.",
		"The more unmatter you find, the more likely you'll get one that leads you to a new gravity well.",
	],
	"ring": [
		"I call this newest invention the Linz flare, after my book club organizer (it's short for Linda).",
		"Use it when you think a piece of unmatter is nearby for a temporary hint.",
		"By the way, don't forget to read through the controls in the lower left.",
	],
	"glow": [
		"Like the Xazer beam, the Searchlight will last until you throw a gravnet.",
		"If you've got charge to spare, you can use them at the same time for extra effectiveness.",
	],
	"map": [
		"Hold down M or 5 at any time to view the sector map.",
		"Sure it's pretty empty now, but you're here to change that, right?",
	],
	"drive": [
		"This hyperdrive should let you reach outer areas much faster.",
		"It will last until you throw a gravnet, and you'll be invulnerable while using it.",
		"I recommend saving one charge to get back, though!",
	],
	"return": [
		"Press Backspace at any time to warp immediately back here. No charge required.",
	],
	"ending": [
		"Congratulations! You have collected enough data to solve the mystery of the unmatter.",
		"Turns out it's made of socks that got lost in the laundry.",
		"The end.\n\nThank you for playing.",
		"If you want to keep playing for some reason, counters will now repair you.",
		"Fly through any counter to refill your hull and charge bars.",
	],
}


