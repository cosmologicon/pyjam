
import pygame
from . import pview


class self:
    pass

def init():
    self.t = 0

def think(dt, kdowns):
    self.t += dt

def draw():
    pview.fill((200, 200, 240))

