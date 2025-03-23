
import pygame
from . import pview, grid, thing


class self:
    pass

def init():
    self.t = 0
    self.you = thing.You((0, 0))

def think(dt, kdowns):
    self.t += dt
    self.you.move(kdowns)
    self.you.think(dt)

def draw():
    pview.fill((200, 200, 240))
    grid.draw()
    self.you.draw()

