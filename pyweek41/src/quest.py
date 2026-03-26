import math
from . import ptext, world
from .pview import T

class self:
	pass

def init():
	self.stage = 0
	self.dstage = 0
	self.alpha = 0

def think(dt):
	if self.stage == 0 and len(world.links) > 0:
		self.stage += 1
	if self.stage == 1 and world.sky > 1:
		self.stage += 1


	if self.stage == self.dstage:
		self.alpha = math.approach(self.alpha, 1, dt)
	else:
		self.alpha = math.approach(self.alpha, 0, dt)
		if self.alpha == 0:
			self.dstage = self.stage

def draw():
	text = None
	if self.dstage == 0:
		text = "Click and drag to link stars."
	if self.dstage == 1:
		text = "Numbers indicate how many links each star should have."
	if text is not None:
		ptext.draw(text, midbottom = T(640, 710), fontsize = T(30), fontname = "Quintessential",
			color = "#7f7faf", shade = 1, owidth = 1, alpha = self.alpha)

	text = f"{world.score}/{len(world.stars)}"
	ptext.draw(text, bottomleft = T(0, 720), owidth = 1, fontsize = T(20), color = "#afafaf")


