
import pygame, math, random
from . import view, pview, grid, thing, ptext, state
from .pview import T


class self:
    pass

def init():
    state.init()
    self.t = 0
    self.haul = 0
    self.engineon = False
    for x, y in grid.wind:
        d = math.interp(math.hypot(x, y), 1, 0, 10, 0.4)
        if grid.wind[(x, y)] == grid.STILL and random.random() < d:
            state.gettables.append(thing.Copper((x, y)))
    returnhome()

def returnhome():
    self.steps = state.maxsteps
    self.engine = state.maxengine
    state.bank += self.haul
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

    if state.you.target == (0, 0):
        state.you.move(move)
        return True
    if move == state.you.windat():
        state.you.move(move)
        return True
    if engineon:
        self.engine -= 1
        grid.wind[state.you.target] = move
        state.you.move(move)
        return True
    if state.you.windat() == grid.STILL:
        if self.steps <= 0:
            return False
        state.you.move(move)
        self.steps -= 1
        return True
    # Trying to move against the wind.
    return False

def athome():
    return state.you.target in [home.pos for home in state.homes]

def canengine():
    return not athome() and self.engine > 0

def think(dt, kdowns):
    from . import scene, reloadscene, shopscene
    self.t += dt
    if "quit" in kdowns:
        reloadscene.init()
        scene.current = reloadscene
    if "engine" in kdowns:
        if canengine():
            self.engineon = not self.engineon
        else:
            self.engineon = False
    move = getmove(kdowns)
    if trymove(move, self.engineon):
        self.engineon = False
        for obj in state.gettables:
            if state.you.target == obj.pos:
                obj.collect()
                self.haul += obj.value
        if athome():
            returnhome()
            state.save()
            shopscene.init()
            scene.current = shopscene
    state.you.think(dt)
    view.camera.target = state.you.pos
    view.think(dt)
    state.gettables = [obj for obj in state.gettables if obj.alive]

def draw():
    pview.fill((200, 200, 240))
    grid.draw()
    for home in state.homes:
        home.draw()
    state.you.draw(self.engineon)
    for obj in state.gettables:
        obj.draw()
    
    text = "\n".join([
        f"Provisions: {self.steps}/{state.maxsteps}",
        f"Engine: {self.engine}/{state.maxengine}",
        f"Current haul: {self.haul}",
        f"Bank: {state.bank}",
    ])
    ptext.draw(text, bottomleft = T(10, 710), fontsize = T(40), owidth = 0.5)
    if self.steps <= 3:
        text = "OUT OF FUEL\nESC: QUIT TO LAST SAVE" if self.steps == 0 else "LOW FUEL"
        ptext.draw(text, midbottom = T(640, 700), fontsize = T(60), owidth = 0.5, shade = 1, color = "red")


