import pygame, math
from OpenGL.GL import *
from OpenGL.GLU import *
from . import ptextgl, state
from .pview import T

class self:
	pass

def init():
	self.aisland = 0
	self.atext = ""

def think(dt):
	aisland = 0
	for island in state.islands:
		if island.distout(state.you.up) < 15:
			aisland = 1
			self.atext = island.name
	self.aisland = math.approach(self.aisland, aisland, 1.5 * dt)

def draw():
	if self.aisland:
		text = "%s Island" % self.atext
		ptextgl.draw(text, midbottom = T(420, 440), fontname = "TradeWinds", fontsize = T(60),
			color = (255, 255, 224), shade = 1.5, owidth = 1, alpha = self.aisland)
	
