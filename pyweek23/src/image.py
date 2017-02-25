from __future__ import division
import pygame, math, os.path
from . import view, util, settings, ptext
from .util import F

imgs = {}
sizetotal = 0
maxsize = 100 << 20
lastcall = { None: 0 }
def get(imgname, scale = 1, angle = 0, cfilter = None):
	global sizetotal
	kangle = 4
	if imgname == "you": kangle = 1
	if imgname == "capsule": kangle = 2
	if imgname == "snake": kangle = 2
	if imgname == "hawk": kangle = 1
	if imgname == "heron": kangle = 1
	if settings.lowres:
		kangle = 90

	angle = kangle * int(round(angle / kangle)) % 360
	key = imgname, scale, angle, cfilter
	lastcall[key] = lastcall[None] = lastcall[None] + 1
	if key in imgs: return imgs[key]
	if cfilter is not None:
		img = get(imgname, scale = scale, angle = angle).convert_alpha()
		array = pygame.surfarray.pixels3d(img)
		array[:,:,:] = (array[:,:] * cfilter).astype(array.dtype)
		del array
	elif scale == 1 and angle == 0:
		if not imgname.endswith("png") and not imgname.endswith("jpg"):
			imgname = os.path.join("data", "img", "%s.png" % imgname)
		img = pygame.image.load(imgname).convert_alpha()
	else:
		img = get(imgname, scale = 1, angle = 0)
		if angle: img = pygame.transform.rotate(img, angle)
		if scale != 1:
			w, h = img.get_size()
			img = pygame.transform.smoothscale(img, (int(round(w * scale)), int(round(h * scale))))
	imgs[key] = img
	sizetotal += img.get_width() * img.get_height() * 4
	clear()
	return img

def clear():
	global sizetotal
	if sizetotal < maxsize:
		return
	if settings.DEBUG:
		print("clearing imgs", len(imgs), sizetotal, pygame.time.get_ticks() * 0.001)
	for key in sorted(imgs, key = lastcall.get):
		img = imgs[key]
		sizetotal -= img.get_width() * img.get_height() * 4
		del imgs[key]
		if sizetotal < 0.5 * maxsize:
			return


def draw(imgname, pos, scale = 1, angle = 0, cfilter = None):
	img = get(imgname, scale = scale, angle = angle, cfilter = cfilter)
	view.screen.blit(img, img.get_rect(center = pos))

def Fdraw(imgname, pos, scale = 1, angle = 0, cfilter = None):
	draw(imgname,
		pos = F(pos),
		scale = util.f * scale,
		angle = angle,
		cfilter = cfilter
	)

def Gdraw(imgname, pos, scale = 1, angle = 0, cfilter = None):
	draw(imgname,
		pos = view.screenpos(pos),
		scale = util.f * view.Z * scale,
		angle = angle,
		cfilter = cfilter
	)

def Bdraw(imgname, pos, s = 120, a = 1, ocolor = (100, 100, 255), showtitle = True):
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
		Fdraw(os.path.join("data", "biopix", imgname + ".jpg"), pos, scale = s / 600)
		name = {
			"1": "Dr. Paulson",
			"2": "Chf. Danilowka",
			"3": "Lt. Jusuf",
			"4": "Dr. Osaretin",
			"5": "Mr. Tannenbaum",
			"6": "Cmdr. Cooper",
			"X": "Mr. Graves",
			"J": "Prof. Jyn",
			"C": "Gen. Cutter",
			"7": "Capt. Gabriel",
			"A": "Capt. Alyx",
		}.get(imgname.split("-")[1])
		if showtitle and name:
			pos = F(pos[0], pos[1] + 0.6 * s)
			ptext.draw(name, midbottom = pos, owidth = 2, fontname = "Lalezar", fontsize = F(12))

