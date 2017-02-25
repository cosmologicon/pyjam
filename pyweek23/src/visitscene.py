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
			fontname = "Lalezar",
			lineheight = 0.66,
			fontsize = F(20),
			width = F(360),
			color = (120, 255, 255),
			gcolor = (40, 244, 244),
			shadow = (1, 1))
		if data["sub%d" % jtext]:
			ptext.draw("(%s)" % data["sub%d" % jtext],
				top = box.top + F(50),
				centerx = box.centerx,
				fontname = "Lalezar",
				fontsize = F(14),
				color = (40, 200, 200),
				shadow = (1, 1))
	image.Bdraw(data["avatar"], pimg, a = util.clamp(self.t * 3 - 0.3, 0, 1), showtitle = False)
	ptext.draw(
		data["title"],
		midtop = F(pimg[0], pimg[1] + 70),
		fontname = "FjallaOne",
		fontsize = F(16),
		alpha = talpha)
	ptext.draw(
		data["name"],
		midtop = F(pimg[0], pimg[1] + 90),
		fontname = "FjallaOne",
		fontsize = F(16),
		color = "yellow",
		alpha = talpha)
	if settings.DEBUG:
		pos = F(475, 5) if settings.portrait else F(849, 5)
		ptext.draw("Encounter #%s\nAffects: %s" % (self.name, data["do"]), topright = pos, fontsize = F(32))



vdata = {}
vdata["1"] = {
	"sname": "Paulson",
	"avatar": "bio-1",
	"title": "Ship's Doctor",
	"name": "Donovan Paulson",
	"lines": [
		"Thank heavens! I never expected anyone to find me this far from the evacuation fleet.",
		"I was a crew member onboard the Starship Hawking. As you probably know, we never completed our mission to close the rift. The ship was destroyed, but most of us managed to escape in these capsules. I imagine you might run into a few more of the crew, scattered like crumbs in the cosmos....",
		"Sorry, I haven't had a good meal in weeks. Look, I've taken some damage. I'll never make it back to the fleet without some hull charge. If I could have some of yours... it's the only shot I've got. What do you say?",
	],
	"fontname": "PassionOne",
	"fontsize": 18,
	"color": "turquoise",
	"opt0": "All right, I can help you.",
	"sub0": "You will lose 3 health bars.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "hp",
}
vdata["2"] = {
	"sname": "Danilowka",
	"avatar": "bio-2",
	"title": "Chief Mechanic",
	"name": "Sergey Danilowka",
	"lines": [
		"I never thought I'd wind up floating through space in one of these capsules. It's all those damn scientists' fault.",
		"You think my team had anything to do with what went wrong on the Hawking? No way, we had our jobs down pat. That weapon malfunctioned. Someone must have made a mistake. It's unthinkable.... to fail with so much on the line.",
		"I'll be honest, I won't get far in this mess. Your lateral weapons just happen to be compatible with the system I've got here. If you could spare them, I just might have a chance of surviving this.",
		"I mean, normally I wouldn't put such a big request on ya, but what the hell. The Earth will be gone soon, and nothing will matter anymore. If I could only hear my wife's voice one last time....",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "All right, I'll help you.",
	"sub0": "You will lose your lateral weapons.",
	"opt1": "I'm sorry, I need everything I have for the dangers ahead.",
	"sub1": "",
	"do": "cshot",
}
vdata["3"] = {
	"sname": "Jusuf",
	"avatar": "bio-3",
	"title": "Security Chief",
	"name": "Boris Jusuf",
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
vdata["4"] = {
	"sname": "Osaretin",
	"avatar": "bio-4",
	"title": "Head Engineer",
	"name": "Obed Osaretin",
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
vdata["5"] = {
	"sname": "Tannenbaum",
	"avatar": "bio-5",
	"title": "Celestial Navigator",
	"name": "Axel Tannenbaum",
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
vdata["6"] = {
	"sname": "Cooper",
	"avatar": "bio-6",
	"title": "First Officer",
	"name": "Lydia Cooper",
	"lines": [
		"Just goes to show, maybe the most important task shouldn't be given to someone just because he's family.",
		"I'm talking about Captain Gabriel, of course. Don't get me wrong, one of the best captains I ever met, but would he have made that same error in judgment if he wasn't Cutter's son?",
		"Oh, Jyn is your daughter? A fine crew member, but I'm afraid I have no idea what became of her after the accident. I hope you find her alive and well. I'm sure you will.",
		"If only I felt confident I could reach my loved ones again....",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "Hopefully this will help.",
	"sub0": "You will lose your short-range weapon.",
	"opt1": "Yes, well, sorry for your situation. Best of luck.",
	"sub1": "",
	"do": "vshot",
}
vdata["7"] = {
	"sname": "Gabriel",
	"avatar": "bio-7",
	"title": "Captain",
	"name": "P. Jim Gabriel",
	"lines": [
		"Well captain, you've come all this way, but you really don't have any idea what you're up against, do you?",
		"You think you can face my father? Why do you think I'm hiding from him here? He was never good with disappointment, and now he's gone completely mad. If he were to discover that the mission failed because of me, there's no telling what he would do to me.",
		"I can't let that secret out. I have to find the rest of the crew. You've found their capsules. Just give me their coordinates. I'll go... reason with them. You can trust me. I'd never hurt anyone, even though it's my own life we're talking about here!",
		"I'll tell you what. I can see that your ship has seen better days. You're in no condition for the fight ahead. But I can help you. I'll make your ship as good as new. Just give me their coordinates. Think about your daughter. Think about Earth. Deal?",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "I suppose I have no choice.",
	"sub0": "You will regain all your downgrades.",
	"opt1": "I don't trust you, and I won't give them up to you.",
	"sub1": "",
	"do": "upgrade",
}
vdata["X"] = {
	"sname": "Graves",
	"avatar": "bio-X",
	"title": "Astro Pilot",
	"name": "Thornton Graves",
	"lines": [
		'''"Everything is possible in space." That was General Cutter's favorite saying.''',
		"Funny, one possibility he never mentioned was getting stranded with no rescue in sight. If he loves space so much, why wasn't he on the mission?",
		"If you ever see him, let him know I'm out of the saving humanity business, if there's even any humanity left to save.",
		"One thing's for sure. I'm not going anywhere with this busted recovery system.",
	],
	"fontname": None,
	"fontsize": 24,
	"color": "turquoise",
	"opt0": "I can help you with that.",
	"sub0": "Decreased invulnerability from damage.",
	"opt1": "I'm sorry, I just can't help you.",
	"sub1": "",
	"do": "charge",
}



	


