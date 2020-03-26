import pygame, numpy, math
from functools import lru_cache
from . import pview

@lru_cache(None)
def getimg0(filename):
	return pygame.image.load("img/%s.png" % filename).convert_alpha()

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

specs = {
	"standing": ["backarm", "stand", "torso", "armdown"],
	"falling": ["backarm", "drop", "torso", "armup"],
	"leap0": ["backarm", "leap", "torso", "armout"],
	"leap1": ["backarm", "leap", "torso", "pointing"],
	"leap2": ["backarm", "leap", "torso", "elbowup"],
	"leap3": ["backarm", "leap", "torso", "armup"],
	"leap4": ["backarm", "leap", "torso", "armdown"],
}

@lru_cache(None)
def youimg0(spec):
	img = pygame.Surface((2020, 2052)).convert_alpha()
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

@lru_cache(200)
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
	



