import pygame
from pygame.locals import *
from . import ptext, view, scene, settings, image, util, background, state, sound
from .util import F

class self:
	pass

def init(name):
	self.name = str(name)
	sound.dplay(vdata[self.name]["sname"] + "1")

	self.t = 0
	self.opt = 0
	self.starting = True
	self.popped = False
	
def think(dt, kdowns, kpressed):
	sound.mplay(1)
	if self.starting:
		self.t += dt
	else:
		self.t -= dt
		if self.t <= 0 and not self.popped:
			self.popped = True
			if self.opt == 0:
				state.downgrade(vdata[self.name]["do"])
				sound.dplay(vdata[self.name]["sname"] + "2")
				if self.name == "7":
					state.saved -= set("123456X")
				else:
					state.saved.add(self.name)
			else:
				sound.dplay(vdata[self.name]["sname"] + "3")
			scene.pop()
	if self.t > 1.5 and self.starting:
		if self.opt == 0:
			if settings.isdown("right", kdowns) or settings.isdown("down", kdowns):
				self.opt = 1
		elif self.opt == 1:
			if settings.isdown("left", kdowns) or settings.isdown("up", kdowns):
				self.opt = 0
		if settings.isdown("action", kdowns):
			self.starting = False
			self.t = 1.5

def draw():
	data = vdata[self.name]
	background.drawfly()
	talpha = util.clamp((self.t - 1) * 2, 0, 1)

	pimg = (85, 85) if settings.portrait else (85, 85)
	psay = F(180, 20) if settings.portrait else F(180, 20)
	pbox = [
		F(50, 600, 380, 80) if settings.portrait else F(32, 360, 380, 80),
		F(50, 700, 380, 80) if settings.portrait else F(424, 360, 380, 80),
	]

	ptext.draw(
		"\n\n".join(data["lines"]),
		topleft = psay,
		width = F(270) if settings.portrait else F(630),
		fontname = data["fontname"],
		fontsize = F(data["fontsize"]),
		color = data["color"],
		shadow = (1, 1),
		alpha = talpha)
	for jtext in range(2):
		box = pygame.Rect(pbox[jtext])
		if self.t < 1.5 and not (jtext == self.opt and not self.starting):
			box.y += F(400 * (1.5 - self.t) ** 2)
		flash = jtext == self.opt and self.t % 0.5 < 0.3
		ocolor = (255, 255, 100) if flash else (200, 200, 0)
		fcolor = (80, 80, 80) if flash else (40, 40, 40)
		view.screen.fill(ocolor, box)
		box.inflate_ip(*F(-6, -6))
		view.screen.fill(fcolor, box)
		ptext.draw(data["opt%d" % jtext],
			top = box.top + F(10),
			centerx = box.centerx,
			fontsize = F(30),
			width = F(360),
			color = (60, 255, 255),
			shadow = (1, 1))
		if data["sub%d" % jtext]:
			ptext.draw("(%s)" % data["sub%d" % jtext],
				top = box.top + F(50),
				centerx = box.centerx,
				fontsize = F(22),
				color = (0, 100, 100),
				italic = True,
				shadow = (1, 1))
	image.Bdraw("bio-0", pimg, a = util.clamp(self.t * 3 - 0.3, 0, 1))
	ptext.draw(
		data["title"],
		midtop = F(pimg[0], pimg[1] + 70),
		fontsize = F(28),
		alpha = talpha)
	ptext.draw(
		data["name"],
		midtop = F(pimg[0], pimg[1] + 90),
		fontsize = F(28),
		alpha = talpha)
	if settings.DEBUG:
		pos = F(475, 5) if settings.portrait else F(849, 5)
		ptext.draw("Encounter #%s\nAffects: %s" % (self.name, data["do"]), topright = pos, fontsize = F(32))



vdata = {}
vdata[1] = {
	"sname": "Paulson",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose 3 health bars.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "hp",
}
vdata[2] = {
	"sname": "Danilowka",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose your C-shots.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "cshot",
}
vdata[3] = {
	"sname": "Jusuf",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose your protective satellite.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "companion",
}
vdata[4] = {
	"sname": "Osaretin",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose your regenerative shield.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "shield",
}
vdata[5] = {
	"sname": "Tannenbaum",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose your targeting missiles.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "missile",
}
vdata[6] = {
	"sname": "Cooper",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose your V-shots.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "vshot",
}
vdata[7] = {
	"sname": "Gabriel",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will regain all your downgrades.",
	"opt1": "I'm sorry, I don't trust you.",
	"sub1": "",
	"do": "upgrade",
}
vdata["X"] = {
	"sname": "Graves",
	"avatar": "bio-0",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"My goodness! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken heavy damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose the ability to charge your weapon.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "charge",
}



	


