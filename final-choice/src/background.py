from __future__ import division
import random, pygame, math, os.path
from . import view, settings, ptext, state, util, pview
from .pview import T

stars = []
nebulas = {}
def init():
	stars.extend([
		(random.uniform(0, 1000000), random.uniform(0, 1000000), random.uniform(0.4, 1))
		for _ in range(10000)
	])
	for name in "crab star tombud spiral".split():
		nebulas[name] = pygame.image.load(os.path.join("data", "astropix", "%s.jpg" % name)).convert_alpha()
#	for j in (0, 1, 2, 3):
#		nebulas["rift-%d" % j] = pygame.image.load("data/img/rift-%d.png" % j).convert_alpha()

def pz(x, y, z):
	x0, y0 = view.x0 + state.xoffset, view.y0
	if settings.portrait:
		return T(240 + y - z * y0, 427 - x + z * x0)
	else:
		return T(427 + x - z * x0, 240 + y - z * y0)

def drawnebulaat(name, x, y, size):
	img = getnebula(name, T(size))
	pview.screen.blit(img, img.get_rect(center = pz(x, y, 0.3)))

def draw(stage = None):
	pview.fill((0, 0, 0))
	if stage == 1:
		drawnebulaat("star", 500, 0, 800)
	if stage == 2:
		drawnebulaat("tombud", 500, 300, 800)
		drawnebulaat("spiral", 2200, -300, 800)
	if stage == 3:
		drawnebulaat("crab", 500, -300, 800)
		drawnebulaat("star", 2200, 300, 800)
	if stage == 4:
		drawnebulaat("tombud", 500, 00, 800)
	N = min(len(stars), int(pview.area * 0.001))
	for x, y, z in stars[:N]:
		px, py = pz(x, y, z)
		px %= pview.w
		py %= pview.h
		color = (int(255 * z),) * 3
		pview.screen.set_at((px, py), color)

def drawfly():
	pview.fill((0, 0, 0))
	N = min(len(stars), int(pview.area * 0.002))
	t = pygame.time.get_ticks() * 0.001 + 100
	for x, y, z in stars[:N]:
		ax = x % 2 - 1
		ay = y % 2 - 1
		r = (x + z * t) / 10 % 1
		kx, ky = util.norm(ax, ay, r * 480)
		px, py = view.screenpos0((kx, ky))
		color = (int(255 * z * r),) * 3
		pview.screen.set_at((px, py), color)
	

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
		img = getnebula("rift-%d" % j, T(640), alpha)
		pview.screen.blit(img, img.get_rect(midright = T(854, 240)))

