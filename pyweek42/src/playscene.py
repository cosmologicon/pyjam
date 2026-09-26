import pygame
from . import pview, thing
from .pview import T

class self: pass

def init():
	self.you = thing.You((0, 0))
	self.hazards = [thing.CircleHazard((3, 1), 2)]

def control(kpressed):
	dx = int("right" in kpressed) - int("left" in kpressed)
	dy = int("down" in kpressed) - int("up" in kpressed)
	self.you.control(dx, dy)

def think(dt):
	self.you.think(dt)
	self.ouch = any(hazard.hitsyou(self.you) for hazard in self.hazards)

def draw():
	pview.fill((20, 20, 20))
	self.you.draw()
	for hazard in self.hazards:
		hazard.draw()
	if self.ouch:
		pview.fill((255, 0, 0, 60))

