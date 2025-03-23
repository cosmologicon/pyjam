
import pygame, math
from . import view, pview, grid, thing, ptext
from .pview import T


class self:
    pass

def init():
    self.t = 0
    self.home = thing.Home()
    self.you = thing.You((0, 0))
    self.gettables = [thing.Copper((2, 2))]
    self.maxsteps = 10
    self.maxengine = 2
    self.bank = 0
    self.haul = 0
    self.engineon = False
    returnhome()

def returnhome():
    self.steps = self.maxsteps
    self.engine = self.maxengine
    self.bank += self.haul
    self.haul = 0

def getmove(kdowns):
    d = (0, 0)
    if "right" in kdowns:
        d = math.vplus(d, grid.E)
    if "left" in kdowns:
        d = math.vplus(d, grid.W)
    if "up" in kdowns:
        d = math.vplus(d, grid.N)
    if "down" in kdowns:
        d = math.vplus(d, grid.S)
    return d

def trymove(move, engineon):
    if move == grid.STILL:
        return False
    if move not in grid.ds:
        return False

    if self.you.target == (0, 0):
        self.you.move(move)
        return True
    if move == self.you.windat():
        self.you.move(move)
        return True
    if engineon:
        self.engine -= 1
        grid.wind[self.you.target] = move
        self.you.move(move)
        return True
    if self.you.windat() == grid.STILL:
        self.you.move(move)
        self.steps -= 1
        return True
    return False

def canengine():
    return self.you.target != self.home.pos and self.engine > 0


def think(dt, kdowns):
    self.t += dt
    if "engine" in kdowns:
        if canengine():
            self.engineon = not self.engineon
        else:
            self.engineon = False
    move = getmove(kdowns)
    if trymove(move, self.engineon):
        self.engineon = False
        for obj in self.gettables:
            if self.you.target == obj.pos:
                obj.collect()
                self.haul += obj.value
        if self.you.target == self.home.pos:
            returnhome()
    self.you.think(dt)
    view.camera.target = self.you.pos
    view.think(dt)
    self.gettables = [obj for obj in self.gettables if obj.alive]

def draw():
    pview.fill((200, 200, 240))
    grid.draw()
    self.home.draw()
    self.you.draw(self.engineon)
    for obj in self.gettables:
        obj.draw()
    
    text = "\n".join([
        f"Provisions: {self.steps}/{self.maxsteps}",
        f"Engine: {self.engine}/{self.maxengine}",
        f"Current haul: {self.haul}",
        f"Bank: {self.bank}",
    ])
    ptext.draw(text, bottomleft = T(10, 710), fontsize = T(40), owidth = 0.5)


