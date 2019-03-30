import pygame, math
from . import pview, ptext, scene, frostscene, stagedata
from .pview import T

class self:
	pass

def init(stage):
	self.stage = stage
	self.text = stagedata.story.get(stage, "INSERT STORY HERE")

def think(dt, controls):
	if controls.mdown:
		scene.push(frostscene, depth1 = 3)
		
def draw():
	pview.fill((255, 255, 255))

	ptext.draw(self.text, center = pview.center, width = T(900), color = "#ffffaa", shade = 1,
		owidth = 0.6, fontsize = T(64), fontname = "GermaniaOne", shadow = (1, 1))

