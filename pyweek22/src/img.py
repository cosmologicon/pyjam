from __future__ import division
import pygame, math
from . import view

splitrotozoom = True

imgs = {}
cachesize = 0
def getimg(name, radius = None, fstretch = 1, angle = 0, alpha = 1, tocache = True):
	global cachesize
	if tocache:
		angle = round(angle / 4) * 4 % 360
		alpha = round(alpha * 16) / 16
		if fstretch != 1:
			fstretch = math.exp(round(math.log(fstretch) * 10) / 10)
	key = name, radius, fstretch, angle, alpha
	if key in imgs:
		return imgs[key]
	if alpha != 1:
		img = getimg(name, radius, fstretch, angle, tocache = tocache).copy()
		img.fill((255, 255, 255, int(alpha * 255)), None, pygame.BLEND_RGBA_MULT)
	elif radius is not None or angle != 0:
		img0 = getimg(name, fstretch = fstretch, tocache = tocache)
		z = radius / (getimg(name).get_width() / 2)
		splitrotozoom = z < 1
		if splitrotozoom:
			img = pygame.transform.rotate(img0, angle)
			s = int(round(img.get_width() * z)), int(round(img.get_height() * z))
			img = pygame.transform.smoothscale(img, s)
		else:
			img = pygame.transform.rotozoom(img0, angle, z)
	elif fstretch != 1:
		img0 = getimg(name)
		size = int(img0.get_width() / fstretch), int(img0.get_height() * fstretch)
		img = pygame.transform.smoothscale(img0, size)
	elif name.startswith("saw"):
		tocache = True
		img = getsaw(int(name[3:]))
	else:
		tocache = True
		img = pygame.image.load("data/img/%s.png" % name).convert_alpha()
	if tocache:
		cachesize += img.get_width() * img.get_height() * 4
		imgs[key] = img
		if cachesize > 256 * 1024 ** 2:
#			print("Emerengency img cache dump!", cachesize, len(imgs))
			clearcache()
	return img

def clearcache():
	global cachesize
	cachesize = 0
	imgs.clear()

def draw(name, screenpos, radius = None, fstretch = 1, angle = 0, alpha = 1, tocache = True):
	img = getimg(name, radius = radius, fstretch = fstretch, angle = angle, alpha = alpha, tocache = True)
	view.screen.blit(img, img.get_rect(center = screenpos))

def drawworld(name, pos, radius, fstretch = 1, angle = 0, alpha = 1):
	draw(name, screenpos = view.screenpos(pos), radius = view.screenlength(radius),
		fstretch = fstretch, angle = angle, alpha = alpha)

def getsaw(n):
	surf = pygame.Surface((20 * n, 20 * n)).convert_alpha()
	center = 10 * n, 10 * n
	surf.fill((0, 0, 0, 0))
	r6 = 10 * n
	r5 = r6 - 20
	r4 = r6 - 10
	r3 = r4 - 20
	r2 = r4 - 25
	r1 = r2 - 10
	thetas = [j * math.tau / (2 * n) for j in range(2 * n)]
	rs = [r6, r5] * n
	ps = [(center[0] + r * math.cos(theta), center[1] + r * math.sin(theta))
		for r, theta in zip(rs, thetas)]
	pygame.draw.polygon(surf, (100, 100, 100), ps)
	rs = [r4, r3] * n
	ps = [(center[0] + r * math.cos(theta), center[1] + r * math.sin(theta))
		for r, theta in zip(rs, thetas)]
	pygame.draw.polygon(surf, (50, 50, 50), ps)
	pygame.draw.circle(surf, (100, 100, 100), center, r + 5)
	pygame.draw.circle(surf, (50, 50, 50), center, r - 5)
	return surf

if __name__ == "__main__":
	import pygame, random
	from . import mhack
	pygame.init()
	view.screen = pygame.display.set_mode((400, 400))
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		view.screen.fill((0, 0, 0))
		t = 0.001 * pygame.time.get_ticks()
		angle = 15 * math.sin(1.23456 * t)
		fstretch = math.exp(0.2 * math.sin(4 * t))
		splitrotozoom = False
		draw("virus", (100, 200), radius = 100, angle = angle, fstretch = fstretch)
		draw("virus", (40, 40), radius = 6, angle = angle, fstretch = fstretch)
		splitrotozoom = True
		draw("virus", (300, 200), radius = 100, angle = angle, fstretch = fstretch)
		draw("virus", (240, 40), radius = 6, angle = angle, fstretch = fstretch)
		draw("simon", (300, 300), radius = 60, alpha = 0.5)
		draw("saw5", (100, 350), radius = 50)
		pygame.display.flip()
	

