import math, pygame
from . import view, pview, grid


class Thing:
    def __init__(self, pos):
        self.pos = pos
        self.t = 0
    
    def think(self, dt):
        self.t += dt


class You(Thing):
    def __init__(self, pos):
        Thing.__init__(self, pos)
        self.target = self.pos

    def move(self, kdowns):
        if "right" in kdowns:
            self.target = math.vplus(self.target, grid.E)
        if "left" in kdowns:
            self.target = math.vplus(self.target, grid.W)
        if "up" in kdowns:
            self.target = math.vplus(self.target, grid.N)
        if "down" in kdowns:
            self.target = math.vplus(self.target, grid.S)

    def think(self, dt):
        if self.target != self.pos:
            self.pos = math.softapproach(self.pos, self.target, 10 * dt, dymin = 0.01)

    def draw(self):
        pygame.draw.circle(pview.screen, (255, 100, 100), view.worldtoscreen(self.pos), view.sizetoscreen(0.25))


