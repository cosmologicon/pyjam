import math, pygame, os.path
from functools import cache
from . import ptext, pview, view, settings

@cache
def loadimg(filename):
	return pygame.image.load(filename)


@cache
def img0(iname, scale = 1, mask = None):
	if scale != 1:
		img = img0(iname, mask = mask)
		w, h = img.get_rect().size
		return pygame.transform.rotozoom(img, 0, scale)
	img = loadimg(os.path.join("img", iname + ".png")).copy()
	if mask is not None:
		maskimg = img.copy()
		maskimg.fill(mask)
		img.blit(maskimg, (0, 0), None, pygame.BLEND_RGBA_MULT)
	return img

def drawimgat(img, pD):
	pview.screen.blit(img, img.get_rect(center = pD))

def drawsymbolatD(symbol, pD, fontsizeD, beta = 1):
	color = math.imix((0, 0, 0), settings.colorcodes[symbol], beta)
	ptext.draw(symbol, center = pD, color = color,
		fontsize = fontsizeD, owidth = 2)
def drawsymbolat(symbol, pD, fontsizeG, beta = 1):
	drawsymbolatD(symbol, pD, view.DscaleG(fontsizeG), beta)

def drawdomeat(pG):
	drawimgat(img0("dome", scale = view.VscaleG / 400, mask = (80, 100, 100)), view.DconvertG(pG))

@cache
def groundimg0():
	s = 15
	surf = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	for px in range(s):
		for py in range(s):
			c = math.imix((40, 30, 20), (70, 60, 50), math.fuzz(1001, px, py))
			for dx in [0, s]:
				for dy in [0, s]:
					surf.set_at((px + dx, py + dy), c)
	return surf

@cache
def groundimg(scale):
	w0, h0 = int(15 * scale), int(15 * scale * math.cos(view.tip))
	surf0 = pygame.transform.smoothscale(groundimg0(), (2 * w0, 2 * h0))
	surf = pygame.Surface((w0, h0)).convert_alpha()
	surf.blit(surf0, (-w0 // 2, -h0 // 2))
	return surf
	

def drawground():
	pview.fill((0, 0, 0))
	if False:
		scale = 0.5 * view.VscaleG * pview.f
		w0, h0 = int(16 * scale), int(16 * scale * math.cos(view.tip))
		surf0 = pygame.transform.smoothscale(groundimg0(), (2 * w0, 2 * h0))
		pview.screen.blit(surf0, (0, 0))
		return
	
	img = groundimg(0.5 * view.VscaleG * pview.f)
	w, h = img.get_size()
	x0, y0 = view.DconvertG((0, 0))
	xmin = -x0 // w
	xmax = (-x0 + pview.w) // w
	ymin = -y0 // h
	ymax = (-y0 + pview.h) // h
	for x in range(xmin, xmax + 1):
		for y in range(ymin, ymax + 1):
			pview.screen.blit(img, (x0 + w * x, y0 + h * y))

def sandcolor(*seed):
	return [
		int(math.fuzzrange(30, 60, 1, *seed)),
		int(math.fuzzrange(15, 30, 2, *seed)),
		int(math.fuzzrange(0, 15, 3, *seed)),
	]
sand = [(
	int(math.fuzzrange(0, 100000, 2001, j)),
	int(math.fuzzrange(0, 100000, 2002, j)),
	math.fuzzrange(0.5, 1, 2003, j),
	sandcolor(2004, j),
) for j in range(10000)]
def drawsand():
	return
	N = 1000
	t = pygame.time.get_ticks() * 0.001
	for x, y, z, color in sand[:N]:
		px = (x + view.DscaleG(-4 * z * t)) % pview.w
		py = (y + view.DscaleG(0.4 * z * t)) % pview.h
		pview.screen.set_at((px, py), color)


