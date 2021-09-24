import random, math, pygame, os.path
from functools import lru_cache
from . import pview, view
from .pview import T

stars = []
def drawstars():
	Nstars = math.ceil(0.003 * pview.area)
	if len(stars) != Nstars:
		del stars[:]
		for jstar in range(Nstars):
			x = random.uniform(0, 1000000)
			y = random.uniform(0, 1000000)
			z = math.mix(0.2, 0.5, jstar / Nstars)
			color0 = 200, random.uniform(200, 255), random.uniform(200, 255)
			a = math.mix(0.2, 1, (jstar / Nstars) ** 4)
			color = math.imix((0, 0, 0), color0, a)
			stars.append((x, y, z, color))
	for x, y, z, color in stars:
		px = T((x - z * view.x0) * 40) % pview.w
		py = T(-(y - z * view.y0) * 40) % pview.h
		pview.screen.set_at((px, py), color)

def mask(img, color):
	cimg = img.copy()
	cimg.fill(color)
	cimg.blit(img, (0, 0), None, pygame.BLEND_RGBA_MULT)
	return cimg

def drawat(img, pos):
	pview.screen.blit(img, img.get_rect(center = pos))

@lru_cache(1000)
def hillimg(color, r, alpha):
	c0 = (color) + (int(round(alpha * 255)),)
	if c0 != (255, 255, 255, 255):
		return mask(hillimg((255, 255, 255), r, 1), c0)
	r0 = 32
	if r != r0:
		return pygame.transform.smoothscale(hillimg(color, r0, alpha), (2 * r, 2 * r))
	img = pygame.Surface((2 * r0, 2 * r0)).convert_alpha()
	for x in range(2 * r0):
		for y in range(2 * r0):
			a = int(math.smoothfadebetween(math.hypot(x - r0 + 0.5, y - r0 + 0.5), 0, 255, r0, 0))
			img.set_at((x, y), (255, 255, 255, a))
	return img


def drawhill(pos, color, r, alpha = 1):
	r = int(round(r))
	alpha = int(alpha * 15) / 15
	drawat(hillimg(color, r, alpha), pos)


def aunit(imgname):
	if "head" in imgname:
		return 1
	if imgname == "segment-menu":
		return 1
	if imgname == "segment":
		return 5
	return 10

@lru_cache(10000)
def getimg0(imgname, angle = 0, scale = None, alpha = 1):
#	print(imgname, angle, scale, getimg0.cache_info().currsize)
	if alpha != 1:
		cmask = (255, 255, 255, math.imix(0, 255, alpha))
		return mask(getimg0(imgname, angle, scale), cmask)
	if scale is not None or angle != 0:
		return pygame.transform.rotozoom(getimg0(imgname), angle, scale)
	return pygame.image.load(os.path.join("img", "%s.png" % imgname)).convert_alpha()
def getimg(imgname, angle = 0, scale = None, alpha = 1):
	if scale is not None:
		scale = math.exp(round(math.log(scale) / 0.05) * 0.05)
	a = aunit(imgname)
	if imgname == "segment-menu":
		imgname = "segment"
	angle = int(round(angle / a) * a) % 360
	alpha = round(alpha * 15) / 15
	return getimg0(imgname, angle, scale, alpha)


def ifactor(imgname):
	if "head" in imgname:
		return 0.032
	if "segment" in imgname:
		return 0.036
	return 0.012

def drawimgscreen(pos, imgname, r, angle, alpha = 1):
	scale = r * ifactor(imgname)
	angle = -math.degrees(angle)
	drawat(getimg(imgname, angle, scale, alpha), pos)

def drawimg(pos, imgname, r, angle, alpha = 1):
	drawimgscreen(view.screenpos(pos), imgname, pview.f * view.scale * r, angle, alpha)

