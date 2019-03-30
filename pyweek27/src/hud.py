from __future__ import division
import pygame, math
from . import pview, ptext, view, render
from .pview import T, I


def fractalimg(color, s):
	img = pygame.Surface((s, s)).convert_alpha()
	if s == 1:
		img.fill(color)
		return img
	img.fill((0, 0, 0, 0))
	subimg = fractalimg(color, I(s / 3))
	dxys = [(0, y) for y in (-1, 0, 1)] + [(x * math.sqrt(3) / 2, y / 2) for x in (-1, 1) for y in (-1, 1)]
	adxys = [(dx, dy) for dx, dy in dxys if dy]
	dxys += [(dx / 2, dy / 2) for dx, dy in dxys]
#	dxys += adxys
	for dx, dy in dxys:
		p = I(s * (1/2 + 1/3 * dx), (s * (1/2 + 1/3 * dy)))
		rect = subimg.get_rect(center = p)
		img.blit(subimg, rect)
	return img

def heximg(s, color):
	img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	img.fill((0, 0, 0, 0))
	ps = [I(s + C, s + S) for C, S in math.CSround(6, 0.99 * s, 0.5)]
	pygame.draw.polygon(img, color, ps, 0)
	return img


bimgcache = {}
def buttonimg(color, size):
	color = tuple(color)
	key = color, size
	if key in bimgcache:
		return bimgcache[key]
	s = I(1.2 * size)
	if size != 200:
		img0 = buttonimg(color, 200)
		img = pygame.transform.smoothscale(img0, (2 * s, 2 * s))
	elif color != (255, 255, 255, 255):
		img = buttonimg((255, 255, 255, 255), size).copy()
		cover = img.copy()
		cover.fill(color)
		img.blit(cover, (0, 0), None, pygame.BLEND_RGBA_MULT)
	else:
		img = heximg(s, color)
		img.blit(fractalimg((100, 100, 100, 5), 2 * s), (0, 0))
	bimgcache[key] = img
	return img

class Button:
	def __init__(self, Fspot, text, color = "white", drawtext = True, shape = None):
		self.Fspot = Fspot
		self.text = text
		self.color = color
		self.rect = view.BrectoverFspot(self.Fspot)
		self.drawtext = drawtext
		self.shape = shape
		self.shapeimg = None
		self.shapeimgs = 0

	def setshape(self, shape):
		self.shape = shape.copy() if shape else shape
		self.shapeimg = None
		self.shapeimgs = 0

	def contains(self, pos):
		return math.length(view.FconvertB(self.Fspot, pos)) < 1

	def draw(self, lit = False, note = None):
		color = self.color
		center, size = self.Fspot
		if note == "0":
			color = render.dim(pygame.Color(color), 8)
			lit = False
		color = ptext._resolvecolor(color, None)
		if not lit:
			color = render.dim(color, 4)
		img = buttonimg(color, T(size))
		rect = img.get_rect(center = T(center))
		pview.screen.blit(img, rect)
		if self.shape is not None:
			s = T(2.5 * size)
			if self.shapeimg is None or s != self.shapeimgs:
				self.shapeimgs = s
				self.shapeimg = heximg(T(size), (255, 255, 255, 255))
				cimg = self.shape.cursorimg(s)
				self.shapeimg.blit(cimg, cimg.get_rect(center = self.shapeimg.get_rect().center), None, pygame.BLEND_RGBA_MIN)
			rect = self.shapeimg.get_rect(center = T(center))
			pview.screen.blit(self.shapeimg, rect)

		if self.drawtext:
			factor = 1.8 * len(self.text) ** -0.4
			ptext.draw(self.text, center = T(center), lineheight = 0.9,
				fontname = "ChelaOne", fontsize = T(factor * size), width = T(2.4 * size), shade = 1, owidth = 0.4, shadow = (1, 1))
		if note is not None:
			x, y = center
			ptext.draw(note, center = T(x + 0.7 * size, y + 0.7 * size),
				fontname = "ChelaOne", fontsize = T(size),
				shade = 1, owidth = 0.4, shadow = (1, 1))
	

