import math, pygame
from . import view, pview, grid, state, graphics


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
        self.glow = 0

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

    def think(self, dt, turbineon):
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
        if math.length(tilt) > 0.1:
            tilt = math.norm(tilt, 0.1)
        self.tilt = math.mix(self.tilt, tilt, 10 * dt)
        if self.athome():
            omega = 0
        elif turbineon:
            omega = 4
        else:
            omega = 1.5
        self.rotoromega = math.approach(self.rotoromega, omega, 1 * dt)
        self.rotortheta += self.rotoromega * dt
        self.glow = math.approach(self.glow, (1 if turbineon else 0), 6 * dt)

    def draw0(self, engineon):
        color = 200, 50, 50
        if engineon:
            color = math.imix(color, (255, 255, 255), 0.5)
        self.drawcircleat(color, 0.25)

    def domecolor(self, fuel):
        if fuel > 3:
            return 180, 30, 150
        if fuel > 0:
            return 200, 20, 50
        return 80, 80, 80

    def draw(self, turbineon, fuel):
        p0 = math.vminus(self.drawpos(), math.vtimes(self.tilt, 0.5))
        p0 = self.drawpos()
        for d in grid.ds:
            f = 0.2 * self.rotortheta + math.fuzz(*d)
            if d in (grid.N, grid.S):
                f = -f
            p = math.vplus(self.drawpos(), math.vtimes(d, 0.25))
            graphics.drawgear(p, f)
        for dx in [-0.4, 0.4]:
            for dy in [-0.4, 0.4]:
                protor = math.vplus(p0, (dx, dy))
                f = self.rotortheta + math.fuzz(dx, dy)
                swap = dx == dy
                graphics.drawrotor(protor, f, swap)
        graphics.drawbody(self.drawpos())
        color = math.imix(self.domecolor(fuel), (240, 240, 240), self.glow)
        graphics.drawdome(self.drawpos(), color)

    def windat(self):
        return grid.wind[self.pos]

def hexps(v0, va, size):
    d0 = math.norm(v0)
    d1 = math.norm(math.cross(v0, va))
    d2 = math.cross(d0, d1)
    ps = [d0, d1, d2, math.vtimes(d0, -1), math.vtimes(d1, -1), math.vtimes(d2, -1)]
    return [(y * size, z * size) for x, y, z in sorted(ps)]


def drawgettable(pos, color, size, highres, *seed):
    t = 0.001 * pygame.time.get_ticks() + 1000 * math.fuzz(1, *seed)
    if math.fuzz(2, *seed) < 0.5:
        t = -t
    dpos = math.CS(20 * t, r = 0.02 * math.sin(0.2 * t))
    pos = math.vplus(pos, dpos)
    if highres:
        def coord(j):
            return math.sin(math.fuzz(1, j, *seed) * math.tau + (0.5 * math.fuzz(2, j, *seed) + 0.5) * t)
        v0 = coord(1), coord(2), coord(3)
        va = coord(4), coord(5), coord(6)
        for d in hexps(v0, va, 0.36 * size):
            graphics.drawdome(math.vplus(pos, d), color, 0.6 * size)
    else:
        graphics.drawdome(pos, color, size)
    


class Gettable(Thing):
    size = 0.5
    value = 0
    def draw(self):
        highres = view.camera.scale > 30
        drawgettable(self.drawpos(), self.color, self.size, highres, *self.pos)
        return
        pos = self.drawpos()
        t = 0.001 * pygame.time.get_ticks() + 1000 * math.fuzz(1, *self.pos)
        if math.fuzz(2, *self.pos) < 0.5:
            t = -t
        dpos = math.CS(20 * t, r = 0.02 * math.sin(0.2 * t))
        pos = math.vplus(pos, dpos)
        if view.camera.scale > 30:
            def coord(j):
                return math.sin(math.fuzz(1, j, *self.pos) * math.tau + (0.5 * math.fuzz(2, j, *self.pos) + 0.5) * t)
            v0 = coord(1), coord(2), coord(3)
            va = coord(4), coord(5), coord(6)
            for d in hexps(v0, va, 0.18):
                graphics.drawdome(math.vplus(pos, d), self.color, 0.3)
        else:
            graphics.drawdome(pos, self.color, 0.5)

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
    size = 0.7


