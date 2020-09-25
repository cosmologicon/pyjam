import pygame, math
from OpenGL.GL import *
from OpenGL.GLU import *
from . import ptextgl, state, view, quest
from .pview import T

class self:
	pass

def init():
	self.aisland = 0
	self.atext = ""

def think(dt):
	aisland = 0
	iname = state.iname()
	if iname is not None:
		aisland = 1
		self.atext = iname
	self.aisland = math.approach(self.aisland, aisland, 1.5 * dt)

def draw():
	alpha0 = 1 - view.hudcutlevel()
	alpha = self.aisland * alpha0
	if alpha:
		text = "%s Island" % self.atext
		ptextgl.draw(text, midbottom = T(640, 700), fontname = "TradeWinds", fontsize = T(90),
			color = (255, 255, 224), shade = 1.5, owidth = 0.2, shadow = (1, 1), alpha = alpha)
	if alpha0:
		objs = quest.objectives()
		if objs:
			text = "\n".join(objs)
#			ptextgl.draw("Objective", midright = T(200, 60), fontname = "PassionOne", fontsize = T(50),
#				color = (224, 224, 255), shade = 1.5, owidth = 1, alpha = alpha0)
#			ptextgl.draw(text, midleft = T(220, 60), width = T(960), fontname = "PassionOne", fontsize = T(38),
#				color = (224, 224, 255), shade = 1.5, owidth = 1.2, alpha = alpha0)
			ptextgl.draw(text, midtop = T(640, 20), width = T(1140), fontname = "PassionOne", fontsize = T(44),
				color = (224, 224, 255), shade = 1.5, owidth = 0.3, shadow = (1, 1), alpha = alpha0)


