
import pygame, math, random
from . import view, pview, grid, thing, ptext, state, sound, marquee
from .pview import T


class self:
    pass

def init():
    state.init()
    marquee.init()
    self.t = 0
    self.haul = 0
    self.hart = 0
    self.engineon = False
    for p in grid.gettables:
        cls = {
            1: thing.Copper,
            2: thing.Silver,
            3: thing.Gold,
            4: thing.Jewel,
        }[grid.gettables[p]]
        state.gettables.append(cls(p))
    for p in grid.artifacts:
        state.gettables.append(thing.Artifact(p))
    returnhome()

def returnhome():
    message = ""
    if self.haul > 0:
        message = f"+${self.haul}"
        state.bank += self.haul
        self.haul = 0
    while state.bank >= state.fuelcosts[state.maxfuel]:
        state.bank -= state.fuelcosts[state.maxfuel]
        state.maxfuel += 1
        message = "Fuel tank upgraded!"
    if self.hart > 0:
        message = "Artifact retrieved!"
        state.artifacts += self.hart
        self.hart = 0
    self.fuel = state.maxfuel
    if message:
        marquee.addline(message)

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

def turbinefuelatyou():
    return state.turbinefuel[grid.strength[state.you.target]]

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
        self.fuel -= turbinefuelatyou()
        grid.setwind(state.you.target, move)
        state.you.move(move)
        sound.play("useengine")
        self.engineon = False
        return True
    if state.you.windat() == grid.STILL:
        if self.fuel <= 0:
            return False
        state.you.move(move)
        self.fuel -= 1
        return True
    # Trying to move against the wind.
    return False

def athome():
    return state.you.target in [home.pos for home in state.homes]

def think(dt, kdowns):
    from . import scene, reloadscene, shopscene
    self.t += dt
    if "quit" in kdowns:
        reloadscene.init()
        scene.current = reloadscene
    if "engine" in kdowns:
        if self.engineon:
            self.fuel -= turbinefuelatyou()
            grid.setwind(state.you.target, grid.STILL)
            sound.play("useengine")
            self.engineon = False
        else:
            if athome():
                pass
            elif self.fuel < turbinefuelatyou():
                sound.play("no")
            elif grid.strength.get(state.you.target, 0) > state.maxturbine:
                sound.play("no")
                print("wind too strong")
            else:
                self.engineon = True
                sound.play("engineon")
    if "flow" in kdowns:
        self.engineon = False
        if state.you.flow() == 0:
            sound.play("no")
        else:
            if athome():
                returnhome()
                state.save()

    move = getmove(kdowns)
    if trymove(move, self.engineon):
        self.engineon = False
        for obj in state.gettables:
            if state.you.target == obj.pos:
                obj.collect()
                if obj.value:
                    self.haul += obj.value
                elif isinstance(obj, thing.Artifact):
                    self.hart += 1
        if athome():
            returnhome()
            state.save()
    state.you.think(dt)
    view.camera.target = state.you.pos
    view.think(dt)
    marquee.think(dt)
    state.gettables = [obj for obj in state.gettables if obj.alive]

def draw():
    pview.fill((100, 100, 120))
    grid.draw()
    for home in state.homes:
        home.draw()
    state.you.draw(self.engineon)
    for obj in state.gettables:
        obj.draw()
    
    text = "\n".join([
        f"Fuel: {self.fuel}/{state.maxfuel}",
        f"Current haul: ${self.haul}",
        f"Bank: ${state.bank}",
        f"Next upgrade: ${state.fuelcosts[state.maxfuel]}",
    ])
    ptext.draw(text, bottomleft = T(10, 710), fontsize = T(40), owidth = 0.5)
    marquee.draw()

    if self.fuel <= 3:
        text = "OUT OF FUEL\nESC: QUIT TO LAST SAVE" if self.fuel == 0 else "LOW FUEL"
        ptext.draw(text, midbottom = T(640, 700), fontsize = T(60), owidth = 0.5, shade = 1, color = "red")


