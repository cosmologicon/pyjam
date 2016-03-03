from __future__ import division
import pygame
from . import util, window, ptext
from .util import debug

imgs = {}
def getimg(imgname, size = None, alpha = None):
	if alpha is None:
		alpha = 1
	if alpha < 0:
		alpha = 0
	elif alpha < 0.2:
		alpha = round(alpha * 80) / 80
	else:
		alpha = round(alpha * 16) / 16
	key = imgname, size, alpha
	if key in imgs:
		return imgs[key]
	if alpha != 1:
		surf = getimg(imgname, size).convert_alpha()
		arr = pygame.surfarray.pixels_alpha(surf)
		arr[:,:] = (arr[:,:] * alpha).astype(arr.dtype)
		del arr
	elif size is not None:
		img0 = getimg(imgname)
		surf = pygame.transform.smoothscale(img0, (size, size))
	else:
		if imgname.startswith("avatar-"):
			surf = pygame.Surface((200, 200)).convert_alpha()
			surf.fill((100, 100, 100))
			ptext.draw(imgname[7:], surf = surf, center = (100, 100), fontsize = 50)
		else:
			surf = pygame.image.load(imgname).convert_alpha()
	imgs[key] = surf
	debug("image cache ", key)
	return surf

def draw(imgname, pos, size = None, scale = None, alpha = None):
	if scale is not None:
		size = int(round(scale * util.f * 2 * window.Z))
	img = getimg(imgname, size, alpha = alpha)
	window.screen.blit(img, img.get_rect(center = pos))

