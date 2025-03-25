import math, pygame
from . import view, pview, grid


class Thing:
    def __init__(self, pos):
        self.pos = pos
        self.t = 0
        self.alive = True
    
    def think(self, dt):
        self.t += dt

    def drawcircleat(self, color, size):
        pygame.draw.circle(pview.screen, color, view.worldtoscreen(self.pos), view.sizetoscreen(size))
        

class Home(Thing):
    def __init__(self):
        Thing.__init__(self, (0, 0))

    def draw(self):
        self.drawcircleat((100, 100, 255), 0.5)
        

class You(Thing):
    def __init__(self, pos):
        Thing.__init__(self, pos)
        self.target = self.pos

    def move(self, dpos):
        self.target = math.vplus(self.target, dpos)

    def flow(self):
        self.start = self.target
        nstep = 0
        while grid.wind[self.target] != grid.STILL:
            self.target = math.vplus(self.target, grid.wind[self.target])
            nstep += 1
            if self.target == self.start:
                break
        return nstep

    def think(self, dt):
        if self.target != self.pos:
            self.pos = math.softapproach(self.pos, self.target, 10 * dt, dymin = 0.01)


    def draw(self, engineon):
        color = 200, 50, 50
        if engineon:
            color = math.imix(color, (255, 255, 255), 0.5)
        self.drawcircleat(color, 0.25)

    def windat(self):
        return grid.wind[self.target]

class Gettable(Thing):
    def draw(self):
        self.drawcircleat(self.color, 0.1)

    def collect(self):
        self.alive = False

class Copper(Gettable):
    color = "#B87333"
    value = 1

class Silver(Gettable):
    color = "silver"
    value = 5

class Gold(Gettable):
    color = "gold"
    value = 10

class Jewel(Gettable):
    color = "purple"
    value = 20



