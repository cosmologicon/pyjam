import functools, math, random, pygame
from . import pview
from . import view, settings
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
def shade(R, r, seed = 0):
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

def cfilter(img, cmask):
	cimg = img.copy()
	cimg.fill(cmask)
	fimg = img.copy()
	fimg.blit(cimg, (0, 0), None, pygame.BLEND_RGBA_MULT)
	return fimg

@cache
def img0(name, scale = 1, angle = 0, cmask = None):
	if cmask is not None:
		return cfilter(img0(name, scale, angle), cmask)
	if scale != 1 or angle != 0:
		return pygame.transform.rotozoom(img0(name, 1, 0), angle, scale)
	return pygame.image.load("img/%s.png" % name).convert_alpha()

def img(name, scale = 1, angle = 0, cmask = None):
	angle = int(angle / 10) * 10 % 360
	surf = img0(name, scale, angle, cmask)
	return surf

def drawimg(pos, *args, **kwargs):
	surf = img(*args, **kwargs)
	pview.screen.blit(surf, dest = surf.get_rect(center = pos))

@cache
def rootsimg(scale, color, f):
	s = 400
	if scale != s:
		return pygame.transform.smoothscale(rootsimg(s, color, f), (2 * scale, 2 * scale))
	if color != None:
		return cfilter(rootsimg(s, None, f), color)
	surf = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for (fw, color) in [(1, (255, 255, 255)), (0.8, (220, 220, 220)), (0.4, (200, 200, 200))]:
		for jangle in range(16):
			fangle = math.clamp(2 * f - jangle/20, 0, 1)
			r = math.mix(0.7, 1, jangle * 1234.56 % 1) * s
			dx0 = math.mix(-0.5, 0.5, jangle * 2345.67 % 1)
			dx1 = math.mix(-0.5, 0.5, jangle * 3456.78 % 1)
			ts = [1/20 * j for j in range(0, 21)]
			ws = [r * 0.3 * (fangle - t) for t in ts]
			xs = [r * 3 * t * (1 - t) * ((1 - t) * dx0 + t * dx1) for t in ts]
			ys = [r * t for t in ts]
			p0s = [(x, y) for x, y, w in zip(xs, ys, ws) if w >= 0]
			if len(p0s) < 2:
				continue
			R = math.R(jangle * math.tau * math.phi)
			ps = [(x + fw * w, y) for (x, y), w in zip(p0s, ws)] + [(x - fw * w, y) for (x, y), w in zip(p0s, ws)][::-1]
			ps = [R(p) for p in ps]
			ps = [(int(s + x), int(s + y)) for x, y in ps]
			pygame.draw.polygon(surf, color, ps)
	return surf

def drawroots(pV0, scale, color, f):
	f = int(f * 16) / 16
	surf = rootsimg(scale, color, f)
	pview.screen.blit(surf, dest = surf.get_rect(center = pV0))

shadesurfs = {}
def getshadesurfs(cameraz):
	from . import state
	if 36 not in shadesurfs:
		s = int(math.ceil(36 * (state.R + 3)))
		shadesurfs[36] = [pygame.Surface((2 * s, 2 * s)).convert_alpha() for _ in range(3)]
		for surf in shadesurfs[36]:
			surf.fill((0, 0, 0, 0))
	if cameraz not in shadesurfs:
		s = int(math.ceil(cameraz * (state.R + 3)))
		shadesurfs[cameraz] = [pygame.transform.smoothscale(surf, (2 * s, 2 * s)) for surf in shadesurfs[36]]
	return shadesurfs[cameraz]
		

def addtree(tree):
	imgs0 = getshadesurfs(36)
	xV0, yV0 = imgs0[0].get_rect().center
	dxG, dyG = tree.pG
	pV = int(xV0 + dxG * 36), int(yV0 - dyG * 36)
	for j, img0 in enumerate(imgs0):
		surf = shade(3 * 36, 8, seed = (dxG, dyG, j))
		img0.blit(surf, surf.get_rect(center = pV), None, pygame.BLEND_RGBA_MAX)
	shadesurfs.clear()
	shadesurfs[36] = imgs0

def drawshades():
	t = 0.001 * pygame.time.get_ticks()
	for j, img in enumerate(getshadesurfs(view.cameraz)):
		xG = 0.3 * math.sin(12.3 * j + 0.6 * t)
		yG = 0.3 * math.sin(23.4 * j + 0.7 * t)
		pview.screen.blit(img, img.get_rect(center = view.VconvertG((xG, yG))))

@cache
def hill(s):
	img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	for x in range(0, 2 * s):
		for y in range(0, 2 * s):
			d = math.hypot(x - s, y - s)
			a = int(math.smoothfadebetween(d, 0, 240, s, 0))
			img.set_at((x, y), (255, 255, 255, a))
	return img

@cache
def spriteimg(s, color, seed):
	if color is not None:
		return cfilter(spriteimg(s, None, seed), color)
	if s != 60:
		return pygame.transform.smoothscale(spriteimg(60, None, seed), (2 * s, 2 * s))
	img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	img.fill((255, 255, 255, 0))
	for _ in range(0):
		x, y = random.randrange(-s, s), random.randrange(-s, s)
		if math.hypot(x, y) >= s: continue
		color = 255, 255, 255, random.randrange(10, 20)
		pygame.draw.line(img, color, (s + x, s + y), (s - x, s - y), 1)
	himg = hill(random.choice([40, 42, 44, 46, 48]))
	img.blit(himg, himg.get_rect(center = (s + random.randint(-1, 1), s + random.randint(-1, 1))), None, pygame.BLEND_RGBA_MAX)
	return img

def drawsprite(pV, s, color):
	seed = random.randrange(0, 40)
	img = spriteimg(s, color, seed)
	pview.screen.blit(img, img.get_rect(center = pV))





csize = 0
def reportcache():
	global csize
	cfuncs = [shade, img0, rootsimg, hill, spriteimg]
	sizes = [func.cache_info().currsize for func in cfuncs]
	if sum(sizes) > csize * 1.5:
		print(sizes)
		for func in cfuncs:
			print(func.cache_info())
		csize = sum(sizes)


