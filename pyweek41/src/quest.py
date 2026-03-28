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
	self.text = None

def do(task):
	self.done.add(task)

def think(dt):
	if len(world.links) > 0:
		do("link")

	text = gettext()
	if text is not None and text == self.text:
		self.alpha = math.approach(self.alpha, 1, dt)
	else:
		self.alpha = math.approach(self.alpha, 0, dt)
	if text is not None and self.alpha == 0:
		self.text = text

def gettext():
	if world.sky <= 1:
		if "link" not in self.done:
			return "Click and drag to link stars."
		else:
			return "Numbers indicate how many links each star must have."
	if world.sky <= 1.5:
		if "remove" not in self.done:
			return "Click and drag on an existing link to remove it."
		else:
			return "Numbers indicate how many links each star must have."
	if world.sky <= 2.0:
		return None
	if world.sky <= 2.5:
		return "Stars labeled Y must have three links that are spaced out.\nNo two links may form an acute angle (<90°) at a Y star."
	if world.sky <= 3.0:
		return "Stars labeled Y must have three links that are spaced out.\nNo two links may form an acute angle (<90°) at a Y star."
	if world.sky <= 3.5:
		return "Stars labeled X must have four links and cannot be connected.\nNo constellation can have more than one X star."
	if world.sky <= 5.5:
		return None
	if world.sky <= 6.0:
		return "The End. Thank you for playing."


def draw():
	if self.text is not None:
		ptext.draw(self.text, midbottom = T(640, 710), fontsize = T(30), fontname = "Quintessential",
			color = "#afafff", shade = 1, owidth = 1, alpha = self.alpha)

	text = f"Magnitude visible: {world.sky:.1f}\nStars correct: {world.score}/{len(world.stars)}"
	ptext.draw(text, bottomleft = T(0, 720), owidth = 1, fontsize = T(20), color = "#af6faf", shade = 1)


