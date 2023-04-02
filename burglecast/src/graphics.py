import os.path, math, pygame
from functools import lru_cache, cache
from . import pview
from .pview import T

@cache
def loadimg(imgname):
	return pygame.image.load(os.path.join("img", f"{imgname}.png")).convert_alpha()

def filterimg(img, mask):
	surf = img.copy()
	surf.fill(mask)
	surf.blit(img, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
	return surf


@lru_cache(1000)
def getimg(imgname, scale, alpha = 255, angle = 0, yscale = 1, shade = 1, mask = None):
	if alpha < 255 or shade < 1 or mask is not None:
		img = getimg(imgname, scale, angle = angle, yscale = yscale)
		r, g, b = mask or (255, 255, 255)
		mask = int(round(r * shade)), int(round(g * shade)), int(round(b * shade)), alpha
		return filterimg(img, mask)
	if yscale != 1:
		img = getimg(imgname, 1, angle = angle)
		w, h = img.get_size()
		size = pview.I(w * scale, h * scale * yscale)
		return pygame.transform.smoothscale(img, size)
	img = loadimg(imgname)
	if angle != 0:
		return pygame.transform.rotozoom(img, angle, scale)
	w, h = img.get_size()
	size = pview.I(w * scale, h * scale)
	return pygame.transform.smoothscale(img, size)


def draw(imgname, pV, scale, alpha = 1, angle = 0, yscale = 1, shade = 1, mask = None):
	scale = math.exp(round(math.log(scale), 2))
	alpha = int(round(alpha * 17)) * 15
	angle = int(round(angle / 10)) * 10 % 360
	img = getimg(imgname, scale, alpha, angle, yscale, shade, mask)
	pview.screen.blit(img, img.get_rect(center = pV))

q = []
def qclear():
	del q[:]

def qfunc(depth, func, *args, **kwargs):
	q.append((depth, func, args, kwargs))

def qdraw(depth, *args, **kwargs):
	qfunc(depth, draw, *args, **kwargs)

def qrender():
	q.sort(key = lambda x: x[0], reverse = True)
	for depth, func, args, kwargs in q:
		func(*args, **kwargs)
	qclear()

def drawblueprint():
	from . import grid
	pview.fill((100, 100, 255))
	color = 115, 115, 255
	x0, y0 = 640, 360
	a = pygame.time.get_ticks() * 0.001 / 30 % 1
	dx, dy = math.R(math.radians(-10), (70 * (3 * 2/math.sqrt(3) + 2 * 1/math.sqrt(3)), 70 * (2 * 1)))
	x0 += a * dx
	y0 += a * dy
	for theta in [math.radians(-10 + 120 * jtheta) for jtheta in (0, 1, 2)]:
		for jline in range(-10, 15):
			d0 = math.R(theta, (-1000, 70 * jline))
			d1 = math.R(theta, (1000, 70 * jline))
			p0 = T(grid.vadd((x0, y0), d0))
			p1 = T(grid.vadd((x0, y0), d1))
			pygame.draw.aaline(pview.screen, color, p0, p1)



