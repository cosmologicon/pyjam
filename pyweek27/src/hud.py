import pygame, math
from . import pview, ptext, view, render
from .pview import T, I


bimgcache = {}
def buttonimg(color, size, lit = False):
	key = color, size, lit
	if key in bimgcache:
		return bimgcache[key]
	s = I(1.2 * size)
	if size != 200:
		img0 = buttonimg(color, 200, lit = lit)
		img = pygame.transform.smoothscale(img0, (2 * s, 2 * s))
	else:
		color = ptext._resolvecolor(color, None)
		if not lit:
			color = render.dim(color, 4)
		img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
		img.fill((0, 0, 0, 0))
		ps = [I(s + C, s + S) for C, S in math.CSround(6, 1.2 * size, 0.5)]
		pygame.draw.polygon(img, color, ps, 0)
		color = render.dim(color, 2)
		ps = [I(s + C, s + S) for C, S in math.CSround(6, 1.0 * size, 0.5)]
		pygame.draw.polygon(img, color, ps, 0)

	
	bimgcache[key] = img
	return img

class Button:
	def __init__(self, Fspot, text, drawtext = True):
		self.Fspot = Fspot
		self.text = text
		self.rect = view.BrectoverFspot(self.Fspot)
		self.drawtext = drawtext

	def contains(self, pos):
		return math.length(view.FconvertB(self.Fspot, pos)) < 1

	def draw(self, lit = False, note = None):
		color = "white"
		center, size = self.Fspot
		if note == "0":
			color = render.dim(pygame.Color(color), 8)
			lit = False
		img = buttonimg(color, T(size), lit = lit)
		rect = img.get_rect(center = T(center))
		pview.screen.blit(img, rect)
		if self.drawtext:
			ptext.draw(self.text, center = T(center), lineheight = 0.9,
				fontname = "ChelaOne", fontsize = T(0.5 * size), width = T(2 * size), shade = 1, owidth = 0.4, shadow = (1, 1))
		if note is not None:
			x, y = center
			ptext.draw(note, center = T(x + 0.7 * size, y + 0.7 * size),
				fontname = "ChelaOne", fontsize = T(size),
				shade = 1, owidth = 0.4, shadow = (1, 1))
	

