import pygame
from . import pview, thing
from .pview import T

class self:
	you = thing.You((0, 0))
	room = thing.Room([(16, -9), (16, 0), (0, 9), (-16, 9), (-16, -0), (0, -9)])


def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.room)

def think(dt):
	pass

def draw():
	pview.fill((20, 20, 60))
	self.room.draw()
	self.you.draw()




