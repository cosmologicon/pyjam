import math
from . import ptext, world
from .pview import T

class self:
	pass

def init():
	self.stage = 0
	self.dstage = 0
	self.alpha = 0
	self.done = set()

def do(task):
	self.done.add(task)

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
	if self.dstage == 2:
		text = "Click and drag on an existing link to remove it.\nNumbers indicate how many links each star should have."
	if self.dstage == 3:
		text = "Stars labeled Y must have three links that are spaced out.\nNo two links may form an acute angle (<90) at a Y star."
	if self.dstage == 4:
		text = "Stars labeled X must have four links.\nNo constellation can have more than one X star."
	if self.dstage == 5:
		text = "Stars labeled Z must have five links.\nEach link must go to a star with a different label."
	if text is not None:
		ptext.draw(text, midbottom = T(640, 710), fontsize = T(30), fontname = "Quintessential",
			color = "#7f7faf", shade = 1, owidth = 1, alpha = self.alpha)

	text = f"Magnitude visible: {world.sky:.1f}\nStars linked: {world.score}/{len(world.stars)}"
	ptext.draw(text, bottomleft = T(0, 720), owidth = 1, fontsize = T(20), color = "#afafaf")


