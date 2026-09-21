import pygame
from . import pview
from .pview import T

class self: pass

def init():
	self.x = 100
	self.y = 100

def control(kpressed):
	dx = int("right" in kpressed) - int("left" in kpressed)
	dy = int("down" in kpressed) - int("up" in kpressed)
	self.vx = 300 * dx
	self.vy = 300 * dy

def think(dt):
	self.x += self.vx * dt
	self.y += self.vy * dt

def draw():
	pview.fill((20, 20, 20))
	pos = T(self.x, self.y)
	pygame.draw.circle(pview.screen, (255, 200, 100), pos, T(10))


