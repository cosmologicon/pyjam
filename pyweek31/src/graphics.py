import functools, math, random, pygame, os.path
from . import pview
from . import view, settings
from .pview import T
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
def groundimg(cameraz, R):
	z0 = 60
	if cameraz != z0:
		s = T(cameraz * (R + 2))
		return pygame.transform.smoothscale(groundimg(z0, R), (2 * s, 2 * s))
	s = z0 * (R + 2)
	surf = pygame.Surface(T(2 * s, 2 * s)).convert_alpha()
	surf.fill((50, 40, 20, 0))
	for pH in view.Hfill(R):
		ps = [T(s + xG * z0, s - yG * z0) for xG, yG in view.GoutlineH(pH, 1.4)]
		color = 50, 40, 20
		pygame.draw.polygon(surf, color, ps)
	for (xH, yH) in view.Hfill(R):
		ps = [T(s + xG * z0, s - yG * z0) for xG, yG in view.GoutlineH((xH, yH))]
		color = 50 - (xH - yH) % 3 * 10, 50, 20
		pygame.draw.polygon(surf, color, ps)
	return surf

def drawground():
	from . import state
	surf = groundimg(view.cameraz, state.R)
	pview.screen.blit(surf, surf.get_rect(center = view.VconvertG((0, 0))))


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
def img0(name, scale = 1, angle = 0, cmask = None, xscale = 1):
	if cmask is not None:
		return cfilter(img0(name, scale, angle, xscale = xscale), cmask)
	if scale != 1 or xscale != 1:
		img1 = img0(name, 1, angle)
		h = pview.I(img1.get_rect().height * scale)
		w = pview.I(img1.get_rect().width * scale * abs(xscale))
		img = pygame.transform.smoothscale(img1, (w, h))
		if xscale < 0:
			img = pygame.transform.flip(img, True, False)
		return img
	if angle != 0:
		return pygame.transform.rotate(img0(name, 1, 0), angle)
	if name.startswith("flower-"):
		return flowerimg0(name.split("-")[1])
	return pygame.image.load(os.path.join("img", "%s.png" % name)).convert_alpha()

def flowerimg0(spec):
	img = img0("flower").copy()
	for j in range(0, len(spec), 2):
		jdH = int(spec[j])
		jcolor = int(spec[j+1])
		img.blit(img0("petal-%d" % jdH, cmask = settings.colors[jcolor]), (0, 0))
	return img


def img(name, scale = 1, angle = 0, cmask = None, xscale = 1):
	angle = int(angle / 10) * 10 % 360
	surf = img0(name, scale, angle, cmask, xscale)
	return surf

def drawimg(pos, *args, **kwargs):
	surf = img(*args, **kwargs)
	pview.screen.blit(surf, dest = surf.get_rect(center = pos))

@cache
def rootsimg(scale, color, f, seed):
	s = 400
	if scale != s:
		return pygame.transform.smoothscale(rootsimg(s, color, f, seed), (2 * scale, 2 * scale))
	if color != None:
		return cfilter(rootsimg(s, None, f, seed), color)
	surf = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for (fw, color) in [(1, (255, 255, 255)), (0.8, (220, 220, 220)), (0.4, (200, 200, 200))]:
		for jangle in range(16):
			fangle = math.clamp(2 * f - jangle/20, 0, 1)
			fseed = jangle * (17.123 + 0.123 * seed)
			r = math.mix(0.7, 1, fseed * 1234.56 % 1) * s
			dx0 = math.mix(-0.5, 0.5, fseed * 2345.67 % 1)
			dx1 = math.mix(-0.5, 0.5, fseed * 3456.78 % 1)
			ts = [1/20 * j for j in range(0, 21)]
			ws = [r * (0.3 * (fangle - t) - 0 * (1 - fw)) for t in ts]
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

def drawroots(pH, scale, color, f):
	xH, yH = pH
	seed = int(1000 * math.cycle(1.23 * xH + 4.56 * yH)) % 3
	f = int(f * 16) / 16
	surf = rootsimg(scale, color, f, seed)
	pview.screen.blit(surf, dest = surf.get_rect(center = view.VconvertH(pH)))

shadesurfs = {}
z0 = 40
def getshadesurfs(cameraz):
	from . import state
	if z0 not in shadesurfs:
		s = T(z0 * (state.R + 3))
		shadesurfs[z0] = [pygame.Surface((2 * s, 2 * s)).convert_alpha() for _ in range(3)]
		for surf in shadesurfs[z0]:
			surf.fill((0, 0, 0, 0))
	if cameraz not in shadesurfs:
		s = T(cameraz * (state.R + 3))
		shadesurfs[cameraz] = [pygame.transform.smoothscale(surf, (2 * s, 2 * s)) for surf in shadesurfs[z0]]
	return shadesurfs[cameraz]
		

def addtree(tree):
	imgs0 = getshadesurfs(z0)
	xV0, yV0 = imgs0[0].get_rect().center
	dxG, dyG = tree.pG
	pV = pview.I(xV0 + pview.f * dxG * z0, yV0 - pview.f * dyG * z0)
	for j, img0 in enumerate(imgs0):
		surf = shade(T(2.5 * z0), T(0.2 * z0), seed = (dxG, dyG, j))
		img0.blit(surf, surf.get_rect(center = pV), None, pygame.BLEND_RGBA_MAX)
	shadesurfs.clear()
	shadesurfs[z0] = imgs0

def drawshades():
	if not settings.nshade:
		return
	t = 0.001 * pygame.time.get_ticks() + 12345
	for j, img in enumerate(getshadesurfs(view.cameraz)):
		if j < settings.nshade:
			xG = 0.3 * math.sin(math.mix(0.5, 0.7, j * math.phi % 1) * t + 1.234 * j)
			yG = 0.3 * math.sin(math.mix(0.6, 0.8, j * 0.234 % 1) * t + 2.345 * j)
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

def drawsprite(pV, s, color, shimmer = True):
	if len(color) > 3:
		color = color[:3] + (int(color[3] / 17) * 17,)
	seed = random.randrange(0, 10) if shimmer else 0
	img = spriteimg(s, color, seed)
	pview.screen.blit(img, img.get_rect(center = pV))


def reset():
	from . import state
	shadesurfs.clear()
	groundimg.cache_clear()
	for tree in state.trees:
		addtree(tree)



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
		print()


