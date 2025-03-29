import math, pygame
from functools import lru_cache
from . import pview, state, ptext
from .pview import T

class self:
    ...

def init(playscene):
    self.playscene = playscene
    self.fuellevel = 0

def think(dt):
    self.fuellevel = math.approach(self.fuellevel, self.playscene.fuel, 10 * dt)

def drawplate(text, center):
    rect = pygame.Rect((0, 0, 140, 64))
    rect.center = center
    pygame.draw.rect(pview.screen, (200, 200, 200), T(rect), border_radius = T(14))
    rect.inflate_ip(-T(6), -T(6))
    pygame.draw.rect(pview.screen, (60, 60, 60), T(rect), border_radius = T(14))
    ptext.draw(text, fontname = "Rye", center = T(center), fontsize = T(40), owidth = 0.2,
        shadow = (1, 1), shade = 1, color = "gray")


Hgauge = 520
Ngauge = 20

@lru_cache(1)
def gauge_img(maxfuel, f):
    surf = pygame.Surface(T(100, Hgauge + 40)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    xwas = [(-3, 8, 0.1), (-3, 6, 0.15), (-3, 4, 0.2), (-10, 2, 0.5), (10, 2, 0.5)]
    y0, y1 = Hgauge + 40, Hgauge + 20 - (Hgauge * maxfuel / Ngauge)
    for x, w, a in xwas:
        color = 255, 255, 255, math.imix(0, 255, a)
        pygame.draw.line(surf, color, T(50 + x, y0), T(50 + x, y1), T(w))
    for n in range(maxfuel + 1):
        y = Hgauge + 20 - (Hgauge * n / Ngauge)
        if n % 5 == 0:
            fontsize, w, lw = 24, 13, 2
        else:
            fontsize, w, lw = 12, 10, 1
        pygame.draw.line(surf, (255, 255, 255, 64), T(50 - w, y), T(50 + w, y), T(lw))
        ptext.draw(f"{n}", surf = surf, fontname = "Rye", fontsize = T(fontsize), owidth = 1,
            midleft = T(64, y))
    return surf

def drawcontrols():
    text = "\n".join([
        "CONTROLS",
        "F1: help",
        "Arrows: move",
        "Space: turbine",
        "Esc: quit",
        "Tab: flow",
    ])
    ptext.draw(text, bottomright = T(1270, 710), fontsize = T(20), fontname = "Notable")
    


def drawunlimited():
    text = "\n".join([
        f"Current nimbite haul: {self.playscene.haul}",
        f"Total nimbite collected: {state.totalbank}",
    ])
    ptext.draw(text, topright = T(1270, 10), fontsize = T(20))
    drawcontrols()        

def draw():
    text = "\n".join([
        f"Current nimbite haul: {self.playscene.haul}",
        f"Fuel tank upgrade: {state.bank}/{state.fuelcosts[state.maxfuel]}",
    ])
    ptext.draw(text, topright = T(1270, 10), fontsize = T(20))
    
    drawcontrols()
    rect = pygame.Rect(T(0, 0, 20, 20 + Hgauge * self.fuellevel / Ngauge))
    rect.midbottom = T(100, pview.centery0 + Hgauge / 2 + 20)
    pygame.draw.rect(pview.screen, (120, 20, 100), rect)
    gauge = gauge_img(state.maxfuel, pview.f)
    pview.screen.blit(gauge, gauge.get_rect(center = T((100, 360))))
    dy = Hgauge / 2 + 20 + 64/2
    drawplate("FUEL", (100, 360 - dy))
    drawplate(f"{self.playscene.fuel}/{state.maxfuel}", (100, 360 + dy))


