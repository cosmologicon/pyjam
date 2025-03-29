import math
from . import ocean, pview, ptext, settings, graphics, grid
from .pview import T

class self:
    pass

def canquit():
    return True

def init():
    self.loaded = False

def finish():
    from . import playscene, scene
    scene.current = playscene

def think(dt, kdowns):
    if not self.loaded:
        self.loaded = not graphics.killtime(0.01)
    if self.loaded and "turbine" in kdowns:
        finish()

def draw():
    ocean.draw()
    ocean.drawstars()
    graphics.drawlightning(0.5)
    ptext.draw(settings.gamename, center = T(640, 200), fontsize = T(140))
    ptext.draw("by Christopher Night\nPyWeek 39\nMusic by Kevin MacLeod",
        center = T(200, 500), fontsize = T(30))

    ptext.draw("F10: change resolution\nF11: toggle fullscreen",
        center = T(1000, 500), fontsize = T(24))

    if self.loaded:
        text = "Press Space to begin"
    else:
        text = "Loading..."
    ptext.draw(text, center = T(640, 640), fontsize = T(60))



