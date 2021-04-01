import functools, math, random, pygame
from . import pview
from . import view
cache = functools.lru_cache(None)

@cache
def grasstexture(size):
	surf = pygame.Surface((size, size)).convert_alpha()
	for x in range(size):
		for y in range(size):
			color = math.imix((40, 25, 0), (25, 40, 0), random.random())
			surf.set_at((x, y), color)
	return surf


def drawgrass():
	s = 400
	img = grasstexture(s)
	xV0, yV0 = view.VconvertG((0, 0))
	for jdx in range(-math.ceil(xV0 / s), math.floor((pview.w - xV0) / s) + 1):
		for jdy in range(-math.ceil(yV0 / s), math.floor((pview.h - yV0) / s) + 1):
			pview.screen.blit(img, (xV0 + jdx * s, yV0 + jdy * s))

@cache
def shade(R, r):
	s = int(math.ceil(R + r))
	surf = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for _ in range(int(2 * (R / r) ** 2)):
		x, y = random.uniform(-1, 1), random.uniform(-1, 1)
		if math.hypot(x, y) > random.uniform(0.5, 1): continue
		pV = int(s + x * R), int(s + y * R)
		rV = int(random.uniform(0.7, 1.4) * r)
		alpha = random.randint(15, 25)
		pygame.draw.circle(surf, (0, 0, 0, alpha), pV, rV)
	return surf

@cache
def img0(name, scale, angle):
	if scale != 1 or angle != 0:
		return pygame.transform.rotozoom(img0(name, 1, 0), angle, scale)
	return pygame.image.load("img/%s.png" % name).convert_alpha()


def img(name, scale = 1, angle = 0):
	angle = int(angle / 10) * 10 % 360
	return img0(name, scale, angle)

def drawimg(pos, *args, **kwargs):
	surf = img(*args, **kwargs)
	pview.screen.blit(surf, dest = surf.get_rect(center = pos))
	


