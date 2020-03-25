import pygame, numpy, math
from functools import lru_cache
from . import pview

@lru_cache(None)
def getimg0(filename):
	return pygame.image.load("img/%s.png" % filename).convert_alpha()

def xform(img, scale, angle, flip):
	if flip:
		img = pygame.transform.flip(img, True, False)
	if angle:
		img = pygame.transform.rotate(img, angle)
	size = pview.I([a * scale / 2000 for a in img.get_size()])
	return pygame.transform.smoothscale(img, size)

@lru_cache(1000)
def getimg(filename, scale, angle = 0, flip = False):
	return xform(getimg0(filename), scale, angle, flip)

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

@lru_cache(None)
def youimg(spec, scale, angle, faceright):
	return xform(youimg0(spec), scale, angle, not faceright)

def colorshift(img, seed):
	img = img.copy()
	arr = pygame.surfarray.pixels3d(img)
	shift = numpy.array([[[1.234 * seed + 2, 1.345 * seed + 3, 1.456 * seed + 4]]]) * 256 % 256
	shifted = 127.0 + 127 * numpy.sin((math.tau / 256) * (arr + shift))
	arr[:,:,:] = shifted.astype(arr.dtype)
	return img

def fade(img, alpha):
	img = img.copy()
	arr = pygame.surfarray.pixels_alpha(img)
	arr[:,:] = (arr * alpha).astype(arr.dtype)
	return img

def you(spec, screenpos, scale, angle, faceright, seed = None, alpha = None):
	angle = int(round(angle)) % 360
	img = youimg(spec, scale, angle, faceright)
	if seed is not None:
		img = colorshift(img, seed)
	if alpha is not None:
		img = fade(img, alpha)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)

def drawimg(filename, screenpos, scale, angle = 0, flip = False):
	angle = int(round(angle)) % 360
	img = getimg(filename, scale, angle, flip)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)
	

