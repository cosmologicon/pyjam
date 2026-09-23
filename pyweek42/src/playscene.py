import pygame
from . import pview, thing
from .pview import T

class self: pass

def init():
	self.you = thing.You((100, 100))

def control(kpressed):
	dx = int("right" in kpressed) - int("left" in kpressed)
	dy = int("down" in kpressed) - int("up" in kpressed)
	self.you.control(dx, dy)

def think(dt):
	self.you.think(dt)

def draw():
	pview.fill((20, 20, 20))
	self.you.draw()


