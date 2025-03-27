import math
from . import ptext
from .pview import T

class self:
    ...

class Line:
    def __init__(self, text):
        self.text = text
        self.t = 0
        self.p1 = math.vplus(self.p0, self.dp)
        self.f = 0
        self.alive = True
    def think(self, dt):
        self.t += dt
        self.f = math.clamp(self.t / self.T0, 0, 1)
        self.alive = self.f < 1
    def draw(self):
        pos = T(math.mix(self.p0, self.p1, self.f))
        alpha = math.interp(self.f, 0.5, 1, 1, 0)
        ptext.draw(self.text, center = pos, fontsize = T(self.fontsize), fontname = self.fontname,
            owidth = 0.5, shade = 1)

class ReturnLine(Line):
    fontsize = 50
    fontname = "Rye"
    T0 = 1.0
    p0 = 640, 640
    dp = 0, -30
    

class BurnLine(Line):
    fontsize = 25
    fontname = "Notable"
    T0 = 1.0
    p0 = 640, 280
    dp = 0, -40

class LowBurnLine(BurnLine):
    p0 = 640, 440

linecounts = {}


def init():
    self.t = 0
    self.lines = []

def addreturnline(text):
    self.lines.append(ReturnLine(text))

def addburnline(text, n, textid="", low=False):
    key = text, textid
    linecounts[key] = linecounts.get(key, 0) + 1
    if linecounts[key] >= n:
        return
    self.lines.append(LowBurnLine(text) if low else BurnLine(text))

def think(dt):
    self.t += dt
    for line in self.lines:
        line.think(dt)
    self.lines = [line for line in self.lines if line.alive]
    
def draw():
    for line in self.lines:
        line.draw()


