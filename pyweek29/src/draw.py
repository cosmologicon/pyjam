import pygame, numpy, math
from functools import lru_cache
from . import pview, view, settings
from .pview import T

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

@lru_cache(None)
def getimg0(filename):
	return pygame.image.load("img/%s.png" % filename).convert_alpha()

@lru_cache(None)
def getbackground0(filename):
	return pygame.image.load("background/%s" % filename).convert_alpha()

def xform(img, scale, angle, hflip, vfactor, colormask):
	if abs(vfactor) != 1:
		w, h = img.get_size()
		size = pview.I([w, h * abs(vfactor)])
		img = pygame.transform.smoothscale(img, size)
	vflip = vfactor < 0
	if hflip or vflip:
		img = pygame.transform.flip(img, hflip, vflip)
	if angle:
		img = pygame.transform.rotate(img, angle)
	size = pview.I([a * scale / 2000 for a in img.get_size()])
	img = pygame.transform.smoothscale(img, size)
	if colormask is not None:
		colorarr = numpy.array(colormask).reshape([1, 1, 3]) / 256.0
		arr = pygame.surfarray.pixels3d(img)
		arr[:,:,:] = (arr * colorarr).astype(arr.dtype)
		del arr
	return img


@lru_cache(1000)
def getimg(filename, scale, angle = 0, flip = False, vfactor = 1, colormask = None):
	return xform(getimg0(filename), scale, angle, flip, vfactor, colormask)

@lru_cache(2)
def getbackground(filename, wmin, hmin):
	img = getbackground0(filename)
	w0, h0 = img.get_size()
	w, h = pview.I(max((wmin, wmin * h0 / w0), (hmin * w0 / h0, hmin)))
	return pygame.transform.smoothscale(img, (w, h))


specs = {
	"standing": ["backarm", "stand", "torso", "armdown"],
	"falling": ["backarm", "drop", "torso", "armup"],
	"leap0": ["backarm", "leap", "torso", "armout"],
	"leap1": ["backarm", "leap", "torso", "pointing"],
	"leap2": ["backarm", "leap", "torso", "elbowup"],
	"leap3": ["backarm", "leap", "torso", "armup"],
	"leap4": ["backarm", "leap", "torso", "armdown"],

	"pose-horiz-0": ["backarm", "leap", "torso", "pointing"],
	"pose-horiz-1": ["backarm", "leap", "torso", "elbowup"],
	"pose-horiz-2": ["backarm", "leap", "torso", "armout"],
	"pose-horiz-3": ["backarm", "leap", "torso", "armdown"],
	"pose-horiz-4": ["backarm", "bound", "torso", "pointing"],
	"pose-horiz-5": ["backarm", "bound", "torso", "elbowup"],
	"pose-horiz-6": ["backarm", "bound", "torso", "armout"],
	"pose-horiz-7": ["backarm", "bound", "torso", "armdown"],
}

@lru_cache(None)
def youimg0(spec):
	img = pygame.Surface((2020, 2152)).convert_alpha()
	img.fill((0, 0, 0, 0))
	for filename in specs[spec]:
		img.blit(getimg0("you-%s" % filename), (0, 0))
	return img


def colorshift(img, seed):
	img = img.copy()
	arr = pygame.surfarray.pixels3d(img)
	shift = numpy.array([[[1.234 * seed + 2, 1.345 * seed + 3, 1.456 * seed + 4]]]) * 256 % 256
	shifted = 127.0 + 127 * numpy.sin((math.tau / 256) * (arr + shift))
	arr[:,:,:] = shifted.astype(arr.dtype)
	return img

@lru_cache(None)
def youimg(spec, scale, angle, faceright, seed = None):
	if seed is not None:
		return colorshift(youimg(spec, scale, angle, faceright), seed)
	return xform(youimg0(spec), scale, angle, not faceright, 1, None)


def fade(img, alpha):
	if alpha == 1:
		return img
	img = img.copy()
	arr = pygame.surfarray.pixels_alpha(img)
	arr[:,:] = (arr * alpha).astype(arr.dtype)
	return img

def you(spec, screenpos, scale, angle, faceright, seed = None, alpha = None):
	angle = int(round(angle)) % 360
	img = youimg(spec, scale, angle, faceright, seed)
	if alpha is not None:
		img = fade(img, alpha)
	if screenpos is not None:
		rect = img.get_rect(center = screenpos)
		pview.screen.blit(img, rect)

def drawimg(filename, screenpos, scale, angle = 0, flip = False, vfactor = 1, colormask = None):
	angle = int(round(angle)) % 360
	vfactor = round(vfactor, 1)
	if vfactor == 0:
		return
	img = getimg(filename, scale, angle, flip, vfactor, colormask)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)

@lru_cache(None)
def getarrowimg0():
	img = pygame.Surface((200, 200)).convert_alpha()
	img.fill((0, 0, 0, 0))
	ps = (100, 0), (160, 50), (100, 200), (40, 50)
	pygame.draw.polygon(img, (0, 0, 0), ps)
	ps = (100, 10), (150, 50), (100, 180), (50, 50)
	pygame.draw.polygon(img, (255, 255, 255), ps)
	return img

@lru_cache(1000)
def getarrowimg(scale, d, color0, f, alpha):
	img = getarrowimg0().copy()
	xs = numpy.arange(float(200)).reshape([200, 1, 1])
	ys = numpy.arange(float(200)).reshape([1, 200, 1])
	mask = ((-ys + 0.9 * abs(xs - 100)) * 0.006 - f) % 1 * 0.4 + 0.6
	colorarr = numpy.array(color0).reshape([1, 1, 3]) / 256.0
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = (arr * mask * colorarr).astype(arr.dtype)
	del arr
	dx, dy = d
	img = pygame.transform.rotate(img, math.degrees(math.atan2(-dx, dy)))
	size = pview.I([a * scale / 200 for a in img.get_size()])
	img = pygame.transform.smoothscale(img, size)
	return fade(img, alpha)

def arrow(screenpos, scale, d, color0, f, alpha):
	f = int(f * 8) % 8 / 8
	img = getarrowimg(scale, d, color0, f, alpha)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)

@lru_cache(10)
def groundtexture0(colormask):
	x0, y0 = 100, 100
	img = pygame.Surface((x0, y0)).convert()
	colorarr = numpy.array(colormask).reshape([1, 1, 3]) / 256.0
	values = 1.0 - 0.15 * numpy.random.rand(x0, y0, 1) - 0.05 * numpy.random.rand(x0, y0, 3)
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = (255 * values * colorarr).astype(arr.dtype)
	return img

@lru_cache(1)
def groundtexture(w, h, offset, colormask):
	w0, h0 = w + 8, h + 8
	wi, hi = w0 // 8, h0 // 8
	img0 = groundtexture0(colormask)
	arr0 = pygame.surfarray.pixels3d(img0)
	xs = (numpy.arange(wi).reshape([wi, 1]) - wi / 2 + offset) / 8
	ys = numpy.arange(hi).reshape([1, hi]) / 2
	W = 1 / (0.5 + ys / 20)
	xs = (xs * W).astype(int) % 100
	ys = (ys * W).astype(int) % 100
	img = pygame.Surface((wi, hi)).convert()
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = arr0[xs,ys,:]
	return pygame.transform.smoothscale(img, (w0, h0))

def background(filename):
	pview.fill((40, 40, 40))
	(x0, y0), (wmin, hmin) = T(view.backgroundspec())
	img = getbackground(filename, wmin, hmin)
	pview.screen.blit(img, img.get_rect(midbottom = (x0, y0)))
	if y0 < pview.height:
		offset = T(view.zoom * view.cx)
		img = groundtexture(view.rrect.left, pview.height - y0, offset, (50, 80, 80))
		pview.screen.blit(img, img.get_rect(midtop = (x0, y0)))

def loadimgs(scale):
	for facingright in (False, True):
		for angle in (-28, -14, 0, 14, 28):
			for pose0 in range(8):
				for j in (2, 1, 0):
					pose = (pose0 + 3 * j) % 8
					seed = 100 * pose + 17
					drawspec = "pose-horiz-%d" % pose
					if j == 0:
						you(drawspec, None, scale, angle, facingright)
					else:
						you(drawspec, None, scale, angle, facingright, seed, 1)
					yield
		you("standing", None, scale, 0, facingright)
		you("falling", None, scale, 0, facingright)




tokill = {}
def killtimeinit():
	global tokill
	youimg.cache_clear()
	tokill = { zoom: loadimgs(T(1.3 * zoom)) for zoom in view.allzooms }

def killtime(dt):
	z = view.zoom if view.zoom in tokill else pickany(tokill)
	if z is None:
		return
	tend = pygame.time.get_ticks() + dt * 1000
	while z in tokill and pygame.time.get_ticks() < tend:
		try:
			next(tokill[z])
		except StopIteration:
			del tokill[z]
			if settings.DEBUG:
				print("done", z, youimg.cache_info())

def finishkill():
	if view.zoom in tokill:
		for _ in tokill[view.zoom]:
			pass
		del tokill[view.zoom]



