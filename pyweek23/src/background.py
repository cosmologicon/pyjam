from __future__ import division
import random, pygame
from . import view, settings, ptext, state
from .util import F

stars = []
nebulas = {}
def init():
	stars.extend([
		(random.uniform(0, 1000000), random.uniform(0, 1000000), random.uniform(0.4, 1))
		for _ in range(10000)
	])
	for name in "crab star tombud spiral".split():
		nebulas[name] = pygame.image.load("astropix/%s.jpg" % name).convert_alpha()

def pz(x, y, z):
	x0, y0 = view.x0 + state.xoffset, view.y0
	if settings.portrait:
		return F(240 + y - z * y0, 427 - x + z * x0)
	else:
		return F(427 + x - z * x0, 240 + y - z * y0)

def draw():
	view.screen.fill((0, 0, 0))
	img = getnebula("star", F(800))
	view.screen.blit(img, img.get_rect(center = pz(500, 0, 0.3)))
	ptext.draw(settings.gamename, center = pz(0, 0, 0.3), color = "#220000", fontsize = F(60), angle = 10)
	ptext.draw("by team Universe Factory", center = pz(0, 160, 0.3), color = "#222222", fontsize = F(40), angle = 10)
	N = min(len(stars), int(view.sx * view.sy * 0.001))
	for x, y, z in stars[:N]:
		px, py = pz(x, y, z)
		px %= view.sx
		py %= view.sy
		color = (int(255 * z),) * 3
		view.screen.set_at((px, py), color)

def getnebula(name, h):
	key = name, h
	if key in nebulas:
		return nebulas[key]
	img0 = nebulas[name]
	w = int(round(img0.get_width() / img0.get_height() * h))
	nebulas[key] = img = pygame.transform.smoothscale(img0, (w, h))
	return nebulas[key]


