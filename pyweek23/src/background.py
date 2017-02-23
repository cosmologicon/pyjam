from __future__ import division
import random, pygame, math
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
	for j in (0, 1, 2, 3):
		nebulas["rift-%d" % j] = pygame.image.load("data/img/rift-%d.png" % j).convert_alpha()

def pz(x, y, z):
	x0, y0 = view.x0 + state.xoffset, view.y0
	if settings.portrait:
		return F(240 + y - z * y0, 427 - x + z * x0)
	else:
		return F(427 + x - z * x0, 240 + y - z * y0)

def draw():
	view.screen.fill((0, 0, 0))
	img = getnebula("star", F(800))
#	view.screen.blit(img, img.get_rect(center = pz(500, 0, 0.3)))
	ptext.draw(settings.gamename, center = pz(0, 0, 0.3), color = "#220000", fontsize = F(60), angle = 10)
	ptext.draw("by team Universe Factory", center = pz(0, 160, 0.3), color = "#222222", fontsize = F(40), angle = 10)
	N = min(len(stars), int(view.sx * view.sy * 0.001))
	for x, y, z in stars[:N]:
		px, py = pz(x, y, z)
		px %= view.sx
		py %= view.sy
		color = (int(255 * z),) * 3
		view.screen.set_at((px, py), color)

def getnebula(name, h, alpha = 1):
	alpha = int(round(alpha * 16)) / 16
	key = name, h, alpha
	if key in nebulas:
		return nebulas[key]
	if alpha == 1:
		img0 = nebulas[name]
		w = int(round(img0.get_width() / img0.get_height() * h))
		nebulas[key] = img = pygame.transform.smoothscale(img0, (w, h))
	else:
		nebulas[key] = img = getnebula(name, h).convert_alpha()
		array = pygame.surfarray.pixels_alpha(img)
		array[:,:] = (array[:,:] * alpha).astype(array.dtype)
		del array
	return nebulas[key]

def drawrift():
	t = pygame.time.get_ticks() * 0.001
	for j in range(3):
		alpha = 0.5 + 0.5 * math.sin((0.3 * t - j / 3) * math.tau)
		img = getnebula("rift-%d" % j, F(640), alpha)
		view.screen.blit(img, img.get_rect(midright = F(854, 240)))

