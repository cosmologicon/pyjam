from __future__ import division
import pygame
from . import pview
from .pview import T

def draw(color, pos, scale):
	x0, y0 = pos
	ps = [T(x0 + a * scale, y0 + b * scale) for a, b in
		[(0.5, 0), (0, 0.25), (-0.5, 0), (0, -0.25)]]
	pygame.draw.polygon(pview.screen, pygame.Color(color), ps)
	pygame.draw.lines(pview.screen, pygame.Color("black"), True, ps, T(0.05 * scale))

