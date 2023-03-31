import os.path, math, pygame
from functools import lru_cache, cache
from . import pview
from .pview import T

@cache
def loadimg(imgname):
	return pygame.image.load(os.path.join("img", f"{imgname}.png")).convert_alpha()

def filterimg(img, mask):
	surf = img.copy()
	surf.fill(mask)
	surf.blit(img, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
	return surf


@lru_cache(1000)
def getimg(imgname, scale, alpha = 255, angle = 0, yscale = 1, shade = 1, mask = None):
	if alpha < 255 or shade < 1 or mask is not None:
		img = getimg(imgname, scale, angle = angle, yscale = yscale)
		r, g, b = mask or (255, 255, 255)
		mask = int(round(r * shade)), int(round(g * shade)), int(round(b * shade)), alpha
		return filterimg(img, mask)
	if yscale != 1:
		img = getimg(imgname, angle = angle)
		w, h = img.get_size()
		size = pview.I(w * scale, h * scale * yscale)
		return pygame.transform.smoothscale(img, size)
	img = loadimg(imgname)
	if angle != 0:
		return pygame.transform.rotozoom(img, angle, scale)
	w, h = img.get_size()
	size = pview.I(w * scale, h * scale)
	return pygame.transform.smoothscale(img, size)


def draw(imgname, pV, scale, alpha = 1, angle = 0, yscale = 1, shade = 1, mask = None):
	scale = math.exp(round(math.log(scale), 2))
	alpha = int(round(alpha * 17)) * 15
	angle = int(round(angle / 10)) * 10 % 360
	img = getimg(imgname, scale, alpha, angle, yscale, shade, mask)
	pview.screen.blit(img, img.get_rect(center = pV))


