from __future__ import division
import pygame
from . import util, window, ptext
from .util import debug

imgs = {}
def getimg(imgname, size = None, alpha = None, boltinfo = None):
	if alpha is None:
		alpha = 1
	if alpha < 0:
		alpha = 0
	elif alpha < 0.2:
		alpha = round(alpha * 80) / 80
	else:
		alpha = round(alpha * 16) / 16
	if boltinfo is not None:
		color, f, outline = boltinfo
		if f is not None:
			f = round(f * 60) / 60
			boltinfo = color, f, outline
	key = imgname, size, alpha, boltinfo
	if key in imgs:
		return imgs[key]
	if alpha != 1:
		surf = getimg(imgname, size, boltinfo = boltinfo).convert_alpha()
		arr = pygame.surfarray.pixels_alpha(surf)
		arr[:,:] = (arr[:,:] * alpha).astype(arr.dtype)
		del arr
	elif size is not None:
		img0 = getimg(imgname, boltinfo = boltinfo)
		surf = pygame.transform.smoothscale(img0, (size, size))
	else:
		if imgname == "bolt":
			color, f, outline = boltinfo
			if color is None and f is None:
				surf = pygame.image.load("data/bolt-outer.png" if outline else "data/bolt-inner.png").convert_alpha()
			else:
				surf = getimg("bolt", boltinfo = (None, None, outline)).copy()
				h = surf.get_height()
				arr = pygame.surfarray.pixels3d(surf)
				if color is not None:
					r, g, b = color[:3]
					arr[:,:,0] = (arr[:,:,0] / 255 * r).astype(arr.dtype)
					arr[:,:,1] = (arr[:,:,1] / 255 * g).astype(arr.dtype)
					arr[:,:,2] = (arr[:,:,2] / 255 * b).astype(arr.dtype)
				if f is not None:
					y = int(round(h * (1 - f)))
					arr[:,:y,:] = 0
				
		elif imgname.startswith("avatar-"):
			surf = pygame.Surface((200, 200)).convert_alpha()
			surf.fill((100, 100, 100))
			ptext.draw(imgname[7:], surf = surf, center = (100, 100), fontsize = 50)
		else:
			surf = pygame.image.load(imgname).convert_alpha()
	imgs[key] = surf
	debug("image cache ", key)
	return surf

def draw(imgname, pos, size = None, scale = None, alpha = None, boltinfo = None):
	if scale is not None:
		size = int(round(scale * util.f * 2 * window.Z))
	img = getimg(imgname, size, alpha = alpha, boltinfo = boltinfo)
	window.screen.blit(img, img.get_rect(center = pos))

