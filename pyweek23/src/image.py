import pygame
from . import view, util
from .util import F

imgs = {}
def get(imgname, scale = 1, angle = 0):
	kangle = 4
	if imgname == "you": kangle = 1

	angle = kangle * int(round(angle / kangle)) % 360
	key = imgname, scale, angle
	if key in imgs: return imgs[key]
	if scale == 1 and angle == 0:
		img = pygame.image.load("data/img/%s.png" % imgname).convert_alpha()
	else:
		img0 = get(imgname, scale = 1, angle = 0)
#		img = pygame.transform.rotozoom(img0, angle, scale)
		img = img0
		if angle: img = pygame.transform.rotate(img, angle)
		if scale != 1:
			w, h = img.get_size()
			img = pygame.transform.smoothscale(img, (int(round(w * scale)), int(round(h * scale))))
	imgs[key] = img
	return imgs[key]

def draw(imgname, pos, scale = 1, angle = 0):
	img = get(imgname, scale = scale, angle = angle)
	view.screen.blit(img, img.get_rect(center = pos))

def Fdraw(imgname, pos, scale = 1, angle = 0):
	draw(imgname,
		pos = F(pos),
		scale = util.f * scale,
		angle = angle
	)

def Gdraw(imgname, pos, scale = 1, angle = 0):
	draw(imgname,
		pos = view.screenpos(pos),
		scale = util.f * view.Z * scale,
		angle = angle
	)
