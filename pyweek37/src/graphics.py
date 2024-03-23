import math, pygame, os.path
from functools import cache, lru_cache
from . import ptext, pview, view, settings, grid

@cache
def loadimg(filename):
#	return pygame.transform.scale2x(pygame.transform.scale2x(pygame.image.load(filename)))
	return pygame.image.load(filename)

@cache
def drawsymbol(symbol):
	img = pygame.Surface((400, 400)).convert_alpha()
	img.fill((0, 0, 0, 0))
	if symbol == "R":
		pygame.draw.circle(img, (0, 0, 0), (200, 200), 126)
		pygame.draw.circle(img, (255, 255, 255), (200, 200), 96)
#		cs = [(max(r, g, b), a) for x in range(400) for y in range(400) for r, g, b, a in [img.get_at((x, y))]]
#		print(symbol, sum(r > 0 and a > 0 for r, a in cs), sum(a > 0 for r, a in cs))
		return img
	if symbol == "O":
		rs = [157] * 4
	if symbol == "Y":
		rs = [196] * 3
	if symbol == "G":
		rs = [196, 90] * 4
	if symbol == "B":
		rs = [184, 92] * 5
	theta0 = 1/8 if symbol == "O" else 1/4
	thetas = [(jtheta / len(rs) - theta0) * math.tau for jtheta in range(len(rs))]
	center = (200, 230) if symbol == "Y" else (200, 200)
	ps = [pview.I(math.CS(theta, r, center = center)) for theta, r in zip(thetas, rs)]
	pygame.draw.polygon(img, (0, 0, 0), ps)
	dr = 0.24
	ps = [pview.I(math.CS(theta, r * (1 - dr), center = center)) for theta, r in zip(thetas, rs)]
	pygame.draw.polygon(img, (255, 255, 255), ps)
#	cs = [(max(r, g, b), a) for x in range(400) for y in range(400) for r, g, b, a in [img.get_at((x, y))]]
#	print(symbol, sum(r > 0 and a > 0 for r, a in cs), sum(a > 0 for r, a in cs))
	return img

@cache
def img0(iname, scale = 1, mask = None, smooth = True):
	if "outline" in iname: mask = None
	if scale != 1:
		img = img0(iname, mask = mask)
		w, h = img.get_size()
		if smooth:
			size = pview.I(w * scale, h * scale)
			return pygame.transform.smoothscale(img, size)
		else:
			return pygame.transform.rotozoom(img, 0, scale)
	if iname.startswith("symbol"):
		img = drawsymbol(iname[7:]).copy()
	else:
		img = loadimg(os.path.join("img", iname + ".png")).copy()
	if mask is not None:
		maskimg = img.copy()
		maskimg.fill(mask)
		img.blit(maskimg, (0, 0), None, pygame.BLEND_RGBA_MULT)
	return img


imgqueue = []
def renderqueue():
	def qkey(item):
		img, (xD, yD) = item
		return yD
	imgqueue.sort(key = qkey)
	for img, pD in imgqueue:
		pview.screen.blit(img, img.get_rect(center = pD))
	del imgqueue[:]

def drawimgat(img, pD, immediate = False):
	if immediate:
		pview.screen.blit(img, img.get_rect(center = pD))
	else:
		imgqueue.append((img, pD))

def outlineH(pH):
	pDs = [view.DconvertG(pG) for pG in grid.GoutlineH(pH)]
	pygame.draw.lines(pview.screen, (0, 255, 255), True, pDs, 1)

def drawcircleH(pH, color, scaleG):
	pD = view.DconvertG(grid.GconvertH(pH))
	pygame.draw.circle(pview.screen, color, pD, view.DscaleG(scaleG))


def drawsymbolatD(symbol, pD, sizeD, strength = 1, palette = None, immediate = False):
	color = math.imix((0, 0, 0), settings.getcolor(symbol, palette), strength)
	scale = sizeD / 400
	img = img0(f"symbol-{symbol}", scale = scale, mask = color, smooth = True)
	drawimgat(img, pD, immediate)

def drawsymbolat(symbol, pD, sizeG, strength = 1, palette = None):
	drawsymbolatD(symbol, pD, view.DscaleG(sizeG), strength, palette)

@cache
def bubbleimg(size, flip = False):
	if flip is True:
		return pygame.transform.rotate(bubbleimg(size), 180)
	width, height = size
	if height != 200:
		w = int(round(width * 200 / height))
		return pygame.transform.smoothscale(bubbleimg((w, 200)), size)
	img = pygame.Surface(size).convert_alpha()
	img.fill((0, 0, 0, 0))
	d = 12
	thetas = [-math.tau * jtheta / 100 for jtheta in range(26)]
	pcurve = [math.CS(theta, 200, center = (width - 200, 200)) for theta in thetas]
	ps = [[0, 0], [0, 200]] + [pview.I(p) for p in pcurve]
	pygame.draw.polygon(img, (10, 10, 10), ps)
	pcurve = [math.CS(theta, 200 - 2 * d, center = (width - 200 + d, 200 - d)) for theta in thetas]
	ps = [[d, d], [d, 200-d]] + [pview.I(p) for p in pcurve]
	pygame.draw.polygon(img, (100, 90, 80), ps)
	return img

# flip = True for supply, flip = False for demand
def drawbubbleatH(pH, symbols, flip):
	hD = view.DscaleG(0.4)
	d = -1 if flip else 1
	xD, yD = view.DconvertG(grid.GconvertH(pH), zG = 0.3)
	xD += d * int(0 * hD)
	yD -= d * int(0.2 * hD)
	wD = pview.I(hD * (0.8 * len(symbols) + 0.9))
	img = bubbleimg((wD, hD), flip)
	rect = img.get_rect(topleft = (xD, yD)) if flip else img.get_rect(bottomright = (xD, yD))
	pview.screen.blit(img, rect)
	yD -= d * int(0.5 * hD)
	xD -= d * int(1.1 * hD)
	for symbol, strength in reversed(symbols):
		drawsymbolatD(symbol, (xD, yD), int(1 * hD), strength, immediate = True)
		xD -= d * int(0.8 * hD)

def drawdomeatG(pG, color, outline = False):
	scale = pview.f * view.VscaleG / 400
	fname = "dome" + ("-outline" if outline else "")
	drawimgat(img0(fname, scale = scale, mask = color), view.DconvertG(pG))

def drawtubeatG(pG, mask, jbeta0, jbeta1, outline = False):
	scale = pview.f * view.VscaleG / 400
	fname = f"tube-{jbeta0}-{jbeta1}" + ("-outline" if outline else "")
	drawimgat(img0(fname, scale = scale, mask = mask), view.DconvertG(pG))

def drawdockatG(pG, jbeta, outline = False):
	scale = pview.f * view.VscaleG / 400
	fname = f"dock-{jbeta}" + ("-outline" if outline else "")
	drawimgat(img0(fname, scale = scale, mask = (120, 100, 80)), view.DconvertG(pG))

def drawbuildatG(pG, jbeta, outline = False):
	scale = pview.f * view.VscaleG / 400
	fname = f"build-{jbeta}" + ("-outline" if outline else "")
	drawimgat(img0(fname, scale = scale), view.DconvertG(pG))
	
def drawdomeatH(pH, color, outline = False):
	drawdomeatG(grid.GconvertH(pH), color, outline)

def drawtubeatH(pH, mask, jbeta0, jbeta1, outline = False):
	drawtubeatG(grid.GconvertH(pH), mask, jbeta0, jbeta1, outline)

def drawdockatH(pH, jbeta, outline = False):
	drawdockatG(grid.GconvertH(pH), jbeta, outline)

def drawbuildatH(pH, jbeta, outline = False):
	drawbuildatG(grid.GconvertH(pH), jbeta, outline)

@cache
def cloudimg(sizeD):
	if sizeD != (16, 16):
		return pygame.transform.smoothscale(cloudimg((16, 16)), sizeD)
	img = pygame.Surface(sizeD).convert_alpha()
	w, h = sizeD
	center = (w - 1) / 2, (h - 1) / 2
	for px in range(w):
		for py in range(h):
			d = math.distance(center, (px, py)) / (w - 1) * 2
			alpha = int(math.smoothinterp(d, 0.5, 255, 1, 0))
			color = 30, 30, 30, alpha
			img.set_at((px, py), color)
	return img

def drawcloudatH(pH):
	xG, yG = grid.GconvertH(pH)
	t = pygame.time.get_ticks() * 0.001
	theta0 = math.fuzzrange(0, 1000, 3000, *pH)
	omega = math.fuzzrange(0.1, 0.2, 3001, *pH)
	yG += 0.12 * math.cycle(theta0 + omega * t)
	theta0 = math.fuzzrange(0, 1000, 3002, *pH)
	omega = math.fuzzrange(0.1, 0.2, 3003, *pH)
	xG += 0.12 * math.cycle(theta0 + omega * t)
	sizeD = view.DscaleG(2), view.DscaleG(2 * math.cos(view.tip))
	drawimgat(cloudimg(sizeD), view.DconvertG((xG, yG), 0.2))

@lru_cache(1)
def fogimg0(size):
	return pygame.Surface(size).convert_alpha()

# We don't care about the contents of key, we just want to cache against it
# so that if any of the contents of key are changed this runs again.
@lru_cache(1)
def fogimg(dmax, *key):
	img = fogimg0(pview.size)
	img.fill((30, 30, 30))
	pHs = [(xH * dmax, yH * dmax) for xH, yH in grid.adjsH]
	pDs = [view.DconvertG(grid.GconvertH(pH)) for pH in pHs]
	pygame.draw.polygon(img, (30, 30, 30, 0), pDs)
	return img

def fog(dmax):
	img = fogimg(dmax + 1, pview.size, view.VscaleG, view.xG0, view.yG0)
	pview.screen.blit(img, (0, 0))

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


