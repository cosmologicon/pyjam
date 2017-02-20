import pygame
from . import view, util
from .util import F

imgs = {}
def get(imgname, scale = 1):
	key = imgname, scale
	if key in imgs: return imgs[key]
	if scale == 1:
		img = pygame.image.load("data/img/%s.png" % imgname).convert_alpha()
	else:
		img0 = get(imgname, scale = 1)
		img = pygame.transform.rotozoom(img0, 0, scale)
	imgs[key] = img
	return imgs[key]

def draw(imgname, pos, scale = 1):
	img = get(imgname, scale = scale)
	view.screen.blit(img, img.get_rect(center = pos))

def Fdraw(imgname, pos, scale = 1):
	draw(imgname,
		pos = F(pos),
		scale = util.f * scale
	)
