import math, pygame
from functools import lru_cache
from . import pview, ptext
from .pview import T

# How long to show a line of dialog by default.
# If we actually get audio recordings we'll use the length of the sound file instead.
def tline(line):
	return 0.3 + 0.08 * len(line)

@lru_cache(1000)
def whoimg(who, size):
	if size is not None:
		return pygame.transform.smoothscale(whoimg(who, None), (size, size))
	return pygame.image.load("img/%s.png" % who)
	

class Dialog:
	def __init__(self):
		self.current = None
		self.currenthelp = ""
		self.t = 0
		self.convolines = []
		self.tconvo = 0
	def run(self, line):
		# TODO: allow for different colors and fonts
		# TODO: allow for sequences of dialog that are longer than one line
		self.current = line
		self.t = 0
	def helptext(self, line):
		self.currenthelp = line
	def startconvo(self, convoname):
		self.convolines.extend(convos[convoname])
	def think(self, dt):
		if self.convolines:
			self.tconvo += dt
			if self.tconvo >= tline(self.convolines[0]):
				self.tconvo = 0
				self.convolines.pop(0)
		else:
			self.tconvo = 0
		self.t += dt
		if self.current and self.t > tline(self.current):
			self.current = None
	def draw(self):
		if self.current is not None:
			alpha = math.dsmoothfade(self.t, 0, tline(self.current), 0.3)
			ptext.draw(self.current, midtop = pview.midtop, width = T(720), fontsize = T(50),
				color = "red", owidth = 2, alpha = alpha)
		if self.currenthelp:
			ptext.draw(self.currenthelp, midtop = T(640, 200), width = T(720), fontsize = T(50),
				color = "blue", owidth = 1)
		if self.convolines:
			line = self.convolines[0]
			alpha = math.dsmoothfade(self.tconvo, 0, tline(line), 0.3)
			who = line[:line.index(":")]
			line = line[line.index(":") + 2:]
			ptext.draw(line, bottomleft = T(400, 700), width = T(640), fontsize = T(44),
				color = (100, 100, 255), owidth = 1, alpha = alpha)
			surf = whoimg(who, T(300))
			pview.screen.blit(surf, surf.get_rect(center = T(300, 660)))
			

dialog = Dialog()

# Module-level functions for shorthand
def run(line):
	dialog.run(line)
def think(dt):
	dialog.think(dt)
def draw():
	dialog.draw()
def helptext(line = ""):
	dialog.helptext(line)
def startconvo(convoname):
	dialog.startconvo(convoname)

convos = {
	"test": [
		"Dorgaz: This stupid thing cost 200 billion zoltons! If you can't get it to work, it's coming out of your paycheck!",
		"Nerdozog: Geez, bite my head off why don't you?!",
		"Alitwon: Let me help you before you hurt yourself.",
	],

}




