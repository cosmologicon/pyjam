import pygame, os
from . import settings, image, ptext, util
from .util import F

pygame.mixer.pre_init(22050, -16, 2, 0)

def init():
	pygame.mixer.set_reserved(4)
	# Channel 0 = dialogue
	# Channel 1 = decision
	# Channel 2 = flying
	# Channel 3 = ballad
	song1 = get("decision", d = "music")
	song2 = get("flying", d = "music")
	pygame.mixer.Channel(1).play(song1, -1)
	pygame.mixer.Channel(2).play(song2, -1)

sounds = {}
def get(sname, d = "sound"):
	key = sname, d
	if key in sounds:
		return sname
	fname = os.path.join("data", d, sname + "." + settings.soundext)
	s = pygame.mixer.Sound(fname)
	sounds[key] = s
	return s

def play(sname):
	get(sname).play()

def think(dt):
	dv = 2 * dt
	talking = pygame.mixer.Channel(0).get_busy()
	tvol = [
		0.8 if mtrack == 1 else 0,
		0.8 if mtrack == 2 else 0,
		0.8 if mtrack == 3 else 0,
	]
	for jtrack, vol in enumerate(tvol, 1):
		if talking: vol *= 0.3
		channel = pygame.mixer.Channel(jtrack)
		v0 = channel.get_volume()
		if vol < v0:
			channel.set_volume(max(v0 - dv, vol))
		elif vol > v0:
			channel.set_volume(min(v0 + dv, vol))

mtrack = None
def mplay(track):
	global mtrack
	mtrack = track
	if track == 3:
		pygame.mixer.Channel(3).play(get("ballad", d = "music"))


def dplay(sname):
	channel = pygame.mixer.Channel(0)
	channel.stop()
	channel.play(get(sname, d = "dialog"))

class Dplayer(object):
	def __init__(self, name):
		self.name = name
		self.jline = 0
		self.alive = True
		self.atime = 0
		self.a = None
		self.text = None
	def think(self, dt):
		if pygame.mixer.Channel(0).get_busy():
			if self.jline:
				self.atime = min(self.atime + 3 * dt, 1)
			return
		self.atime = max(self.atime - 3 * dt, 0)
		if self.atime:
			return
		lines = Dlines[self.name]
		if self.jline >= len(lines):
			self.alive = False
			return
		sname, self.a, self.font, self.text = lines[self.jline]
		dplay(sname)
		self.jline += 1
	def draw(self):
		if not self.text:
			return
		if self.a is not None:
			pos = (56, 800) if settings.portrait else (100, 426)
			image.Bdraw(self.a, pos, s = 90, a = self.atime)
		fontname, fontsize, color = {
			"N": ("FjallaOne", 21, (200, 200, 255)),
		}.get(self.font, (None, 28, "white"))
		fontsize = F(fontsize)
		width = F(340) if settings.portrait else F(540)
		pos = F(110, 850) if settings.portrait else F(160, 472)
		ptext.draw(self.text, bottomleft = pos, width = width,
			fontname = fontname, fontsize = fontsize, color = color, shadow = (1, 1),
			alpha = self.atime)
		

Dlines = {}
Dlines["intro"] = [
	["Prologue1", None, "N", "Earth was in peril. A rift in spacetime was tearing through the cosmos, headed straight for the solar system."],
	["Prologue2", "bio-0", "N", "Under the command of General Maxwell Cutter of Earth space fleet, a new weapon was developed to seal the rift."],
	["Prologue3", "bio-0", "N", "The Starship Hawking, commanded by Cutter's son, Captain Gabriel, set out on the deadly mission to deploy the weapon and save humanity. The ship never returned."],
	["Prologue4", None, "N", "While the evacuation of Earth is underway, General Cutter himself is nowhere to be found."],
	["Prologue5", "bio-0", "N", "As Earth's end looms near, Captain Alyx, mother of one of the Hawking crew, receives a message from her daughter. Find me at the rift."],
]

Dlines["climax"] = [
	["C1", "bio-C", "C", "Noooo! This can't be happening!"],
	["C2", "bio-J", "J", "It's almost over.... The rift is closing.... uh oh."],
	["C3", "bio-J", "J", "There's an interdimensional mass imbalance. It won't close until something from our side goes through. At least fifty tons. A missile won't do."],
	["C4", "bio-J", "J", "General, get away from the rift! It's extremely unstable until something enters it."],
	["C5", "bio-C", "C", "I can't! I've lost engines! I've got less than a minute before I'm pulled into the gravity well!"],
	["C6", "bio-J", "J", "Wait, that's perfect! Your ship has enough mass, once you hit the rift, it'll close for good!"],
	["C7", "bio-J", "C", "My ship? What about me?! Won't that kill me?"],
	["C8", "bio-J", "J", "I'm sorry, General. It's you or the Earth now. It's the lesser of two evils."],
	["C9", "bio-C", "C", "Curse you, Alyx! Curse you, Jyn! Curse you Eaaaaaarth!"],
]
Dlines["climax2"] = [
	["C10", "bio-J", "J", "Mother, no!"],
]

Dlines["B"] = [
	["B1", None, "N", "Earth was saved, but Jyn set off to locate the remaining survivors of the Hawking, and was never heard from again."],
]
Dlines["D"] = [
	["D1", None, "N", "Jyn and Alyx returned to Earth and received a heroes' welcome. And the mysteries of what lies beyond the rift remained locked away from humanity forever."],
]
Dlines["E"] = [
	["E1", None, "N", "With a heavy heart, Jyn took General Cutter into custody and returned to Earth, along with the rest of the crew of the Starship Hawking."],
	["E2", None, "N", "Cutter's account of what he had seen beyond the rift allowed Jyn to develop a interdimensional hyperdrive, that in time would enable humanity to reach beyond the stars...."],
]

