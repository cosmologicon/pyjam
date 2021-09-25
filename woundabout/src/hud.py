import math
from . import ptext
from .pview import T

class self:
	current = None
	t = 0

def show(text):
	self.current = text
	self.t = 0

def think(dt):
	self.t += dt

def draw():
	if self.current is not None and self.t < 1.5:
		y = math.fadebetween(self.t, 0, 700, 1.5, 660)
		alpha = min(math.fadebetween(self.t, 0, 0, 0.2, 1), math.fadebetween(self.t, 1, 1, 1.5, 0))
		if alpha > 0:
			ptext.draw(self.current, midbottom = T(640, y), fontsize = T(36),
				color = (255, 230, 200), owidth = 0.5,
				shade = 1, shadow = (1, 1), alpha = alpha)
	
