import pygame
from . import pview, ptext, state
from .pview import T

class self:
    ...

def init():
    self.t = 0

def think(dt, kdowns):
    self.t += dt
    from . import scene, playscene
    if self.t > 0.7 and scene.current is not playscene:
        playscene.init()
        state.load()
        scene.current = playscene
       

def draw():
    pview.fill((40, 20, 20))
    ptext.draw("RELOADING", center = pview.center, fontsize = T(80),
        color = "red", owidth = 1, shade = 1)


