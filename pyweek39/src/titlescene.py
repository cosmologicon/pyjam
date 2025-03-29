import math
from . import ocean, pview, ptext, settings, graphics, grid, sound, view
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
    sound.play("begin")

def think(dt, kdowns):
    if not self.loaded:
        self.loaded = not graphics.killtime(0.01)
    if self.loaded and "turbine" in kdowns:
        finish()

def draw():
    ocean.draw()
    view.camera.x0 = 0
    view.camera.y0 = 0
    view.camera.scale = 200
    graphics.drawhome((0, 0))

    ocean.drawstars()
    graphics.drawlightning(0.5)
    ptext.draw(settings.gamename, center = T(640, 120), fontsize = T(140))
    ptext.draw("by Christopher Night\nPyWeek 39\nMusic by Kevin MacLeod",
        center = T(240, 500), fontsize = T(30))

    ptext.draw("F10: change resolution\nF11: toggle fullscreen",
        center = T(1280 - 240, 500), fontsize = T(32), fontname = "Jockey", lineheight = 0.7)

    if self.loaded:
        text = "Press Space to begin"
    else:
        text = "Loading..."
    ptext.draw(text, center = T(640, 640), fontsize = T(60))



