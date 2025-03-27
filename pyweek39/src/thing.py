import math, pygame
from . import view, pview, grid, state


class Thing:
    def __init__(self, pos):
        self.pos = pos
        self.t = 0
        self.alive = True
    
    def think(self, dt):
        self.t += dt

    def drawpos(self):
        return self.pos

    def drawcircleat(self, color, size):
        pygame.draw.circle(pview.screen, color, view.worldtoscreen(self.drawpos()), view.sizetoscreen(size))
        

class Home(Thing):
    def __init__(self):
        Thing.__init__(self, (0, 0))

    def draw(self):
        self.drawcircleat((100, 100, 255), 0.5)
        

class You(Thing):
    def __init__(self, pos):
        Thing.__init__(self, pos)
        self.targets = [pos]
        self.marker = pos
        self.tilt = (0, 0)
        self.rotoromega = 0
        self.rotortheta = 0

    def athome(self):
        return self.pos in [home.pos for home in state.homes]

    def drawpos(self):
        return self.marker

    def move(self, dpos):
        self.pos = math.vplus(self.pos, dpos)
        self.targets.append(self.pos)

    def snapto(self, pos = None):
        self.targets = [self.pos]
        self.marker = self.pos
        self.tilt = (0, 0)
        self.rotoromega = 0

    def flow(self):
        self.start = self.pos
        nstep = 0
        while grid.wind[self.pos] != grid.STILL:
            self.move(grid.wind[self.pos])
            nstep += 1
            if self.pos == self.start:
                break
        return nstep

    def think(self, dt):
        if len(self.targets) > 1 or self.marker != self.pos:
            pathlen = math.distance(self.marker, self.targets[0]) + len(self.targets) - 1
            pathlen = math.softapproach(pathlen, 0, 10 * dt, dxmax = 40 * dt, dymin = 0.01)
            n, f = divmod(pathlen, 1)
            pfrom = self.marker
            while len(self.targets) > n + 1:
                pfrom = self.targets.pop(0)
            target = self.targets[0]
            dp = math.vminus(pfrom, target)
            self.marker = math.vplus(target, math.norm(dp, f))
        tilt = math.vminus(self.pos, self.drawpos())
        self.tilt = math.mix(self.tilt, tilt, 10 * dt)
        omega = 0 if self.athome() else 3
        self.rotoromega = math.approach(self.rotoromega, omega, 5 * dt)
        self.rotortheta += self.rotoromega * dt

    def draw0(self, engineon):
        color = 200, 50, 50
        if engineon:
            color = math.imix(color, (255, 255, 255), 0.5)
        self.drawcircleat(color, 0.25)

    def draw(self, engineon):
        p0 = math.vminus(self.drawpos(), math.vtimes(self.tilt, 0.5))
        for dx in [-0.5, 0.5]:
            for dy in [-0.5, 0.5]:
                protor = math.vplus(p0, (dx, dy))
                theta = self.rotortheta + math.tau * math.fuzz(dx, dy)
                if dx == dy:
                    theta = -theta
                dps = math.CSround(2, r = 0.3, jtheta0 = theta / 2)
                ps = [view.worldtoscreen(math.vplus(protor, dp)) for dp in dps]
                pygame.draw.line(pview.screen, (150, 150, 150), *ps, view.sizetoscreen(0.02))
                pygame.draw.circle(pview.screen, (200, 200, 200), view.worldtoscreen(protor), view.sizetoscreen(0.05))
        p = view.worldtoscreen(self.drawpos())
        r = view.sizetoscreen(0.3)
        pygame.draw.circle(pview.screen, (200, 50, 50), p, r)

    def windat(self):
        return grid.wind[self.pos]

class Gettable(Thing):
    size = 0.2
    value = 0
    def draw(self):
        self.drawcircleat(self.color, self.size)

    def collect(self):
        self.alive = False

class Copper(Gettable):
    color = "#B87333"
    value = 1

class Silver(Gettable):
    color = "silver"
    value = 3

class Gold(Gettable):
    color = "gold"
    value = 6

class Jewel(Gettable):
    color = "purple"
    value = 12

class Artifact(Gettable):
    color = "black"
    size = 0.3


