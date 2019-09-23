import math
from . import pview, ptext
from .pview import T

# How long to show a line of dialog by default.
# If we actually get audio recordings we'll use the length of the sound file instead.
def tline(line):
	return 0.3 + 0.08 * len(line)

class Dialog:
	def __init__(self):
		self.current = None
		self.t = 0
	def run(self, line):
		# TODO: allow for different colors and fonts
		# TODO: allow for sequences of dialog that are longer than one line
		self.current = line
		self.t = 0
	def think(self, dt):
		self.t += dt
		if self.current and self.t > tline(self.current):
			self.current = None
	def draw(self):
		if self.current is not None:
			alpha = math.dsmoothfade(self.t, 0, tline(self.current), 0.3)
			ptext.draw(self.current, midtop = pview.midtop, width = T(720), fontsize = T(50),
				color = "red", owidth = 2, alpha = alpha)

dialog = Dialog()

# Module-level functions for shorthand
def run(line):
	dialog.run(line)
def think(dt):
	dialog.think(dt)
def draw():
	dialog.draw()
