import math
from . import ptext
from .pview import T

class self:
    ...

class Line:
    def __init__(self, text, T0, p0, dp):
        self.text = text
        self.T0 = T0
        self.t = 0
        self.p0 = p0
        self.p1 = math.vplus(p0, dp)
        self.f = 0
        self.alive = True
    def think(self, dt):
        self.t += dt
        self.f = math.clamp(self.t / self.T0, 0, 1)
        self.alive = self.f < 1
    def draw(self):
        pos = T(math.mix(self.p0, self.p1, self.f))
        alpha = math.interp(self.f, 0.5, 1, 1, 0)
        ptext.draw(self.text, center = pos, fontsize = T(50), owidth = 0.5, shade = 1)



def init():
    self.t = 0
    self.lines = []

def addline(text):
    self.lines.append(Line(text, 1, (640, 640), (0, -30)))

def think(dt):
    self.t += dt
    for line in self.lines:
        line.think(dt)
    self.lines = [line for line in self.lines if line.alive]
    
def draw():
    for line in self.lines:
        line.draw()


