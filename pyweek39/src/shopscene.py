import math, pygame
from . import pview, playscene, scene, sound, state, ptext
from .pview import T

class self:
    ...


def init():
    self.jopt = 1
    self.alive = True
    self.nopts = 3

def p(jopt):
    if jopt == 0:
        return 100, 600
    else:
        return 150, 100 + jopt * 100

def done():
    state.save()
    scene.current = playscene
    self.alive = False
    sound.play("shopdone")

def act(jopt):
    if jopt == 0:
        done()
    elif jopt == 1:
        cost = state.stepcosts[state.maxsteps]
        if cost <= state.bank:
            state.bank -= cost
            state.maxsteps += 1
            sound.play("buy")
        else:
            sound.play("no")
    elif jopt == 2:
        cost = state.enginecosts[state.maxengine]
        if cost <= state.bank:
            state.bank -= cost
            state.maxengine += 1
            sound.play("buy")
        else:
            sound.play("no")

def think(dt, kdowns):
    playscene.think(dt, set())
    if not self.alive:
        return
    if "quit" in kdowns:
        done()
    if "engine" in kdowns:
        act(self.jopt)
    if "up" in kdowns:
        self.jopt -= 1
    if "down" in kdowns:
        self.jopt += 1
    self.jopt %= self.nopts

def draw():
    playscene.draw()
    pview.fill((220, 220, 220, 200))
    texts = [
        "Done",
        f"Upgrade max fuel: {state.maxsteps} (${state.stepcosts[state.maxsteps]})",
        f"Upgrade turbine: {state.maxengine} (${state.enginecosts[state.maxengine]})",
    ]
    ptext.draw(f"Bank: ${state.bank}", topleft = T(50, 50), fontsize = T(60), color = "white", owidth = 1)
    for jopt in range(self.nopts):
        ptext.draw(texts[jopt], midleft = T(p(jopt)), fontsize = T(60), color = "blue", owidth = 1)
    pcursor = math.vplus(p(self.jopt), (-20, 0))
    pygame.draw.circle(pview.screen, (0, 100, 255), T(pcursor), T(10))

    
