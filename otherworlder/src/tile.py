from __future__ import division
import pygame, numpy
from . import pview, view
from .pview import T

def recolortile(img0, color):
	color = tuple(color)[:3]
	img = img0.copy()
	w, h = img.get_size()
	arr = pygame.surfarray.pixels3d(img)
	red = arr[:,:,0] - arr[:,:,1]
	arr[:,:,0] -= red
	arr[:,:,:] += (numpy.array(color).reshape((1, 1, 3)) / 255.0 * red.reshape(w, h, 1)).astype(arr.dtype)
	return img


cache = {}
def gettileimg(color, scale):
	key = color, scale
	if key in cache:
		return cache[key]
	if scale is None:
		img = pygame.image.load("img/tile0.png").convert_alpha()
	elif color is None:
		img0 = gettileimg(None, None)
		w = int(round(scale))
		h = int(round(scale * img0.get_height() / img0.get_width()))
		img = pygame.transform.smoothscale(img0, (w, h))
	else:
		img = recolortile(gettileimg(None, scale), color)
	cache[key] = img
	return img

def getimg(name, scale = None, recolor = None):
	key = name, scale, recolor
	if key in cache:
		return cache[key]
	if recolor is not None:
		img0 = getimg(name, scale)
		img = recolortile(img0, recolor)
	elif scale is not None:
		img0 = getimg(name)
		w = int(round(scale))
		h = int(round(scale * img0.get_height() / img0.get_width()))
		img = pygame.transform.smoothscale(img0, (w, h))
	else:
		img = pygame.image.load("img/%s.png" % name).convert_alpha()
	cache[key] = img
	return img

def draw(color, pV):
	color = tuple(color)[:3]
	scaleP = T(1.2 * view.IscaleG)
	img = gettileimg(color, scaleP)
	xP, yP = T(pV)
	rect = img.get_rect()
	rect.center = xP, yP + int(0.15 * scaleP)
	pview.screen.blit(img, rect)
#	pygame.draw.circle(pview.screen, (255, 127, 0), (xP, yP), 3)

