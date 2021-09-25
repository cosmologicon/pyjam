import random, math, pygame, os.path
from functools import lru_cache
from . import pview, view
from .pview import T

stars = []
def drawstars():
	Nstars = math.ceil(0.001 * pview.area)
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


jframemax = 20
cloudr0 = 120
@lru_cache(1000)
def cloudimg(color, jcloud, jframe, scale0 = None):
	if scale0 != None:
		img0 = cloudimg(color, jcloud, jframe, None)
		w, h = img0.get_size()
		w = int(round(w * scale0))
		h = int(round(h * scale0))
		return pygame.transform.smoothscale(img0, (w, h))
	if jframe > 0 or color != (255, 255, 255):
		scale = math.mix(1, 0.2, (jframe / jframemax))
		angle = int(math.fuzzrange(-360, 360, 123, jcloud) * jframe / jframemax)
		alpha = math.imix(0, 255, jframe / jframemax)
		img0 = pygame.transform.rotozoom(cloudimg((255, 255, 255), jcloud, 0), angle, scale)
		return mask(img0, color + (alpha,))
	img = pygame.Surface((cloudr0, cloudr0)).convert_alpha()
	img.fill((255, 255, 255, 0))
	for jhill in range(60):
		d = int(math.fuzzrange(0.1, 0.2, jhill, jcloud, 0) * cloudr0)
		x = int(math.fuzzrange(0, cloudr0 - 2 * d, jhill, jcloud, 1))
		y = int(math.fuzzrange(0, cloudr0 - 2 * d, jhill, jcloud, 2))
		if math.distance((x + d, y + d), (cloudr0 / 2, cloudr0 / 2)) > cloudr0 / 2 - d:
			continue
		img.blit(hillimg(color, d, 0.2), (x, y))
	return img


def drawcloud(pos, r, t, f = 1, color = (200, 200, 200)):
	scale = view.scale * pview.f * r * 5 / cloudr0
	scale = math.exp(round(math.log(scale), 1))
	for k in range(int(f * 5)):
		a = 3 * t + 1234.567 * k
		jcloud, fframe = divmod(a, 1)
		jcloud %= 10
		jframe = int(fframe * jframemax)
		img = cloudimg(color, jcloud, jframe, scale)
		drawat(img, view.screenpos(pos))

def drawflare(pos, r, t, f = 1, color = (200, 200, 200)):
	theta = 0
	a = math.mix(0.2, 1, math.cycle(t * 4))
	ps = [
		math.CS(theta-math.tau/4, a * 0.1 * r, center = pos),
		math.CS(theta, a * 2.5 * r, center = pos),
		math.CS(theta+math.tau/4, a * 0.1 * r, center = pos),
	]
	ps = [view.screenpos(p) for p in ps]
	color = color + (20,)
	pygame.draw.polygon(pview.screen, color, ps)


def aunit(imgname):
	if "head" in imgname:
		return 1
	if imgname == "segment-menu":
		return 1
	if imgname in ["segment", "tail"]:
		return 5
	return 10

@lru_cache(10000)
def getimg0(imgname, angle = 0, scale = None, alpha = 1):
#	print(imgname, angle, scale, getimg0.cache_info().currsize)
	if alpha != 1:
		cmask = (255, 255, 255, math.imix(0, 255, alpha))
		return mask(getimg0(imgname, angle, scale), cmask)
	if scale is not None or angle != 0:
		img0 = getimg0(imgname)
		if angle == 0:
			w, h = img0.get_size()
			w = int(round(w * scale))
			h = int(round(h * scale))
			return pygame.transform.smoothscale(img0, (w, h))
		return pygame.transform.rotozoom(img0, angle, scale)
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
	if imgname == "tail":
		return 0.036
	if "frames" in imgname:
		return 0.0086 * 200 / 120
	return 0.012

def drawimgscreen(pos, imgname, r, angle, alpha = 1):
	scale = r * ifactor(imgname)
	angle = -math.degrees(angle)
	drawat(getimg(imgname, angle, scale, alpha), pos)

def drawimg(pos, imgname, r, angle, alpha = 1):
	drawimgscreen(view.screenpos(pos), imgname, pview.f * view.scale * r, angle, alpha)

