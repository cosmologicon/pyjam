import pygame, math
from OpenGL.GL import *
from OpenGL.GLU import *
from . import ptextgl, state, view, quest, settings
from .pview import T

class s:
	pass
self = s()

def init():
	self.aisland = 0
	self.atext = ""
	self.acontrol = 0
	self.acontroltext = None
	
	self.otext = None
	self.oalpha = 0
	self.hintalpha = 0

	for island in state.islands:
		text = "%s Island" % island.name
		ptextgl.draw(text, midbottom = T(640, 9999), fontname = "TradeWinds", fontsize = T(90),
			color = (255, 255, 224), shade = 1.5, owidth = 0.2, shadow = (1, 1))


def think(dt, hint):
	aisland = 0
	iname = state.iname()
	if iname is not None:
		aisland = 1
		self.atext = iname
	self.aisland = math.approach(self.aisland, aisland, 1.5 * dt)
	acontroltext = quest.controlinfo()
	acontrol = 1 if self.acontroltext == acontroltext is not None else 0
	self.acontrol = math.approach(self.acontrol, acontrol, 2 * dt)
	if self.acontrol == 0:
		self.acontroltext = acontroltext

	hintalpha = 1 if settings.easymode or hint else 0
	self.hintalpha = math.approach(self.hintalpha, hintalpha, 1 * dt)


	obj = "\n".join(quest.objectives())
	if obj != self.otext:
		self.oalpha = math.approach(self.oalpha, 0, 0.5 * dt)
		if self.oalpha == 0:
			self.otext = obj
	elif self.otext:
		self.oalpha = math.approach(self.oalpha, 1, 0.5 * dt)
		

def draw():
	alpha0 = 1 - view.hudcutlevel()
	alpha = self.aisland * alpha0
	if alpha and quest.shownames():
		text = "%s Island" % self.atext
		ptextgl.draw(text, midbottom = T(640, 712), fontname = "TradeWinds", fontsize = T(90),
			color = (255, 255, 224), shade = 1.5, owidth = 0.2, shadow = (1, 1), alpha = alpha)
	alpha = self.acontrol * alpha0
	if alpha:
		ptextgl.draw(self.acontroltext, midleft = T(20, 360), fontname = "PassionOne", fontsize = T(60),
			color = (224, 224, 255), shade = 1.5, owidth = 0.3, shadow = (1, 1), alpha = alpha)

	alpha = alpha0 * self.oalpha * self.hintalpha
	if alpha and self.otext:
		ptextgl.draw(self.otext, midtop = T(640, 20), width = T(1140), fontname = "PassionOne", fontsize = T(44),
			color = (224, 224, 255), shade = 1.5, owidth = 0.3, shadow = (1, 1), alpha = alpha)

	alpha = alpha0 * quest.titlealpha()
	if alpha:
		ptextgl.draw(settings.gamename, center = T(900, 300), fontname = "TradeWinds", fontsize = T(50),
			color = (224, 224, 255), shade = 1.5, owidth = 0.3, shadow = (1, 1), alpha = alpha)
		ptextgl.draw("by Christopher Night\nComposer: Mary Bichner",
			center = T(900, 400), fontname = "Caveat", fontsize = T(44),
			color = (224, 224, 255), shade = 1.5, owidth = 0.3, shadow = (1, 1), alpha = alpha)



