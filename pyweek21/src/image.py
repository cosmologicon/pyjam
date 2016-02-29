import pygame
from . import util, window, ptext
from .util import debug

imgs = {}
def getimg(imgname, size = None):
	key = imgname, size
	if key in imgs:
		return imgs[key]
	if size is not None:
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

def draw(imgname, pos, size = None, scale = None):
	if scale is not None:
		size = int(round(scale * util.f * 2 * window.Z))
	img = getimg(imgname, size)
	window.screen.blit(img, img.get_rect(center = pos))
	
	
