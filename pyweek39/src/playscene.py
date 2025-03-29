
import pygame, math, random
from . import view, pview, grid, thing, ptext, state, sound, marquee, hud, ocean, graphics
from .pview import T


class self:
    pass

def init():
    state.init()
    marquee.init()
    hud.init(self)
    self.t = 0
    self.levelt = 0
    self.ainfot = 0
    self.haul = 0
    self.hart = 0
    self.turbineon = False
    self.overlay = None
    self.foverlay = 0
    self.zoom = True
    for p in grid.gettables:
        cls = {
            1: thing.Copper,
            2: thing.Silver,
            3: thing.Gold,
            4: thing.Jewel,
        }[grid.gettables[p]]
        state.addgettable(cls(p))
    for p in grid.artifacts:
        state.addgettable(thing.Artifact(p))
    returnhome(False)
    state.softsave()

def canquit():
    return state.you.pos in [home.pos for home in state.homes]

def returnhome(playsound = True):
    message = ""
    sname = None
    if self.haul > 0:
        message = f"+{self.haul} Nimbite"
        state.bank += self.haul
        state.totalbank += self.haul
        self.haul = 0
        sname = "bank"
    if not unlimitedfuel():
        while state.bank >= state.fuelcosts[state.maxfuel]:
            state.bank -= state.fuelcosts[state.maxfuel]
            state.maxfuel += 1
            message = "Fuel tank upgraded!"
            sname = "upgrade"
            self.levelt = 0
    if self.hart > 0:
        message = "Artifact retrieved!"
        state.artifacts += self.hart
        self.hart = 0
        sname = "upgrade"
        self.ainfot = 0
    self.fuel = state.maxfuel
    if message:
        marquee.addreturnline(message)
    if sname:
        sound.play(sname)

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
    return state.turbinefuel[grid.strength[state.you.pos]]

def worldat(pos, dpos = (0, 0)):
    return math.vplus(pos, dpos) in grid.gridset

def unlimitedfuel():
    return state.artifacts >= 8

def burn(dfuel):
    if unlimitedfuel():
        return
    if self.fuel > 0 and self.fuel - dfuel <= 0:
        sound.play("nofuel")
    elif self.fuel > 3 and self.fuel - dfuel <= 3:
        sound.play("lowfuel")
    self.fuel -= dfuel

def refuel(dfuel):
    self.fuel = min(self.fuel + dfuel, state.maxfuel)

def trymove(move, turbineon):
    if move == grid.STILL:
        return False
    if move not in grid.ds:
        return False

    if state.you.pos == (0, 0):
        sound.play("move")
        state.you.move(move)
        return True
    if not worldat(state.you.pos, move):
        marquee.addburnline("OUT OF BOUNDS", 10)
        sound.play("no")
        return

    if move == state.you.windat():
        sound.play("move")
        state.you.move(move)
        return True
    if turbineon:
        marquee.addburnline(f"-{turbinefuelatyou()} FUEL", 5)
        burn(turbinefuelatyou())
        grid.setwind(state.you.pos, move)
        state.you.move(move)
        sound.play("useturbine")
        self.turbineon = False
        self.foverlay = 0
        self.overlay = move
        return True
    if state.you.windat() == grid.STILL:
        if self.fuel <= 0:
            marquee.addburnline("OUT OF FUEL", 5)
            sound.play("no")
            return False
        sound.play("move")
        state.you.move(move)
        burn(1)
        marquee.addburnline("-1 FUEL", 20)
        return True
    # Trying to move against the wind.
    marquee.addburnline("MUST MOVE DOWNSTREAM", 5)
    sound.play("no")
    return False

def checkarrive():
    if state.you.pos in state.gettables:
        obj = state.gettables[state.you.pos]
        obj.collect()
        sound.play("get")
        refueling = state.artifacts >= 5
        if obj.value:
            self.haul += obj.value
            marquee.addburnline(f"+{obj.value} NIMBITE", 5, low = True)
            if refueling:
                refuel(obj.value)
        elif isinstance(obj, thing.Artifact):
            marquee.addburnline("GOT ARTIFACT", 10)
            self.hart += 1
            if refueling:
                refuel(1000)
        del state.gettables[state.you.pos]
    if state.you.athome():
        returnhome()
        state.save()


def think(dt, kdowns):
    from . import scene, reloadscene, shopscene, howtoscene
    self.t += dt
    self.levelt += dt
    self.ainfot += dt
    if self.overlay is not None:
        self.foverlay += 2.0 * dt
        if self.foverlay >= 1:
            self.overlay = None
    if "quit" in kdowns:
        init()
        state.load()
        self.fuel = state.maxfuel
        state.you.snapto()
        view.snapto(state.you.pos)
        marquee.addreturnline("Game reloaded")
        sound.play("reload")
        return
    if "howto" in kdowns:
        howtoscene.init()
        scene.current = howtoscene
    if "turbine" in kdowns:
        if self.turbineon:
            marquee.addburnline(f"-{turbinefuelatyou()} FUEL", 5)
            burn(turbinefuelatyou())
            grid.setwind(state.you.pos, grid.STILL)
            sound.play("useturbine")
            self.turbineon = False
        else:
            state.maxturbine = [1, 2, 2, 3, 3, 3, 3, 3, 3][state.artifacts]
            if state.you.athome():
                pass
            elif grid.strength.get(state.you.pos, 0) > state.maxturbine:
                marquee.addburnline("WIND TOO STRONG", 20, state.maxturbine)
                sound.play("no")
            elif self.fuel < turbinefuelatyou():
                marquee.addburnline(f"-{turbinefuelatyou()} FUEL", 5)
                sound.play("no")
            else:
                self.turbineon = True
                sound.play("turbineon")
    if "flow" in kdowns:
        self.turbineon = False
        if state.you.flow() == 0:
            marquee.addburnline(f"NO WIND", 5)
            sound.play("no")
        else:
            checkarrive()
            sound.play("flow")

    move = getmove(kdowns)
    if trymove(move, self.turbineon):
        self.turbineon = False
        checkarrive()
    state.you.think(dt, self.turbineon)
    if "zoom" in kdowns and state.artifacts >= 2:
        self.zoom = not self.zoom
    view.camera.zoom = not(state.artifacts >= 2 and state.you.athome() and self.zoom)
    view.camera.target = state.you.marker
    view.think(dt)
    marquee.think(dt)
    hud.think(dt)

levelhelptext = {
    6: "Arrow keys or WASD: move.\nCollect nimbite gas and return to Anyport to upgrade fuel tank.",
    7: "In windy areas, you must move downstream, but it requires no fuel to do so.",
    8: "In windy areas, you must move downstream, but it requires no fuel to do so.",
    9: "Turbine: Press Space or Enter, then a direction. Create or redirect windy areas.",
    10: "Press Space twice to turn a windy area into a calm area.",
    11: "Press Tab on a windy area to flow downstream.",
    12: "Artifacts are due north, south, east, and west of home.",
    13: "Collect 1 artifact to upgrade turbine.",
}
artifactinfo = {
    1: "1 Artifact collected\nTurbine upgraded to level 2.",
    2: "2 Artifacts collected\nMap unlocked. Press 2 to toggle.\nMap is visible while at Anyport.",
    3: "3 Artifacts collected\nTurbine upgraded to level 3.",
    5: "5 Artifacts collected\nCollecting nimbite refuels you.",
    8: "8 Artifacts collected\nUnlimited fuel!\nTHE END\nThank you for playing!",
}

def draw():
    ocean.draw()
    for home in state.homes:
        home.draw()
    state.you.draw(self.turbineon, self.fuel)
    for pos, obj in state.gettables.items():
        if view.onscreen(pos):
            obj.draw()
    grid.draw()
#    ocean.drawstars()
    if self.overlay is not None:
        grid.drawoverlay(self.overlay, self.foverlay)

    flightning = math.interp(math.length(state.you.pos), 18, 0, 40, 0.3)
    graphics.drawlightning(flightning)

    if unlimitedfuel():
        hud.drawunlimited()
    else:
        hud.draw()
    marquee.draw()

    if state.maxfuel in levelhelptext:
        alpha = math.dsmoothfade(self.levelt, 0, 60, 0.4)
        if alpha > 0:
            ptext.draw(levelhelptext[state.maxfuel], midtop = T(640, 10), fontsize = T(25),
                width = T(700), color = (200, 200, 255), alpha = alpha)

    if state.artifacts in artifactinfo:
        alpha = math.dsmoothfade(self.levelt, 0, 60, 0.4)
        if alpha > 0:
            ptext.draw(levelhelptext[state.maxfuel], midtop = T(640, 10), fontsize = T(25),
                width = T(700), color = (200, 200, 255), alpha = alpha)
    
    if self.fuel <= 3:
        if self.fuel == 0:
            if state.maxfuel <= 12:
                text = "OUT OF FUEL\nESC: QUIT TO LAST SAVE"
            else:
                text = "OUT OF FUEL"
        else:
            text = "LOW FUEL"
        ptext.draw(text, midbottom = T(640, 700), fontsize = T(30), color = "#ff7f7f")



