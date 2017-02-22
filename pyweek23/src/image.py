from __future__ import division
import pygame, math
from . import view, util
from .util import F

imgs = {}
def get(imgname, scale = 1, angle = 0):
	kangle = 4
	if imgname == "you": kangle = 1
	if imgname == "capsule": kangle = 2

	angle = kangle * int(round(angle / kangle)) % 360
	key = imgname, scale, angle
	if key in imgs: return imgs[key]
	if scale == 1 and angle == 0:
		if not imgname.endswith("png") and not imgname.endswith("jpg"):
			imgname = "data/img/%s.png" % imgname
		img = pygame.image.load(imgname).convert_alpha()
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

def Bdraw(imgname, pos, s = 120, a = 1, ocolor = (100, 100, 255)):
	w = util.clamp((3 * a - 1) * s, 1, s)
	h = util.clamp((3 * a) * s, 1, s)
	rect = pygame.Rect(0, 0, w, h)
	rect.center = pos
	if a < 1:
		pygame.draw.rect(view.screen, (100, 100, 100), F(rect))
	rect.inflate_ip(8, 8)
	ocolor = tuple(int(c * (0.8 + 0.2 * math.sin(0.01 * pygame.time.get_ticks()))) for c in ocolor)
	pygame.draw.rect(view.screen, ocolor, F(rect), F(2))
	if a == 1:
		Fdraw("biopix/" + imgname + ".jpg", pos, scale = s / 600)

