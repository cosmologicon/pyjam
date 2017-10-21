from __future__ import division
import pygame, random, math
from . import pview, view, settings, state

def init():
	if settings.lowres:
		state.effects.append(Mist(8))
#		state.effects.append(Mist(-8))
	else:
		state.effects.append(Mist(20))
		state.effects.append(Mist(8))
		state.effects.append(Mist(-8))
		state.effects.append(Mist(-20))

class Mist(object):
	def __init__(self, z):
		self.y = 0
		self.z = z
		self.surf = None
	def makesurf(self):
		self.w = pview.w
		scale = 20 * view.scale(self.z)
		w0, h0 = int(pview.w / scale) + 5, int(pview.h / scale) + 5
		surf = pygame.Surface((w0, h0)).convert_alpha()
		surf.fill((200, 200, 255, 0))
		arr = pygame.surfarray.pixels_alpha(surf)
		y0 = h0 / 2 + 5 * pview.f
		for y in range(h0):
			a0 = 100 + 600 * (y - y0) / h0
			for x in range(w0):
				arr[x,y] = math.clamp(a0 + random.randint(-20, 20), 0, 200)
		del arr
		surf = pygame.transform.smoothscale(surf, (int(w0 * scale), int(h0 * scale)))
		self.surf = pygame.Surface(pview.size).convert_alpha()
		self.surf.fill((0, 0, 0, 0))
		self.surf.blit(surf, surf.get_rect(center = self.surf.get_rect().center))
	def draw(self):
		if self.surf is None or self.w != pview.w:
			self.makesurf()
		x0, _ = view.toscreen(0, 0, self.z)
		x0 %= pview.w
		pview.screen.blit(self.surf, (x0, 0))
		pview.screen.blit(self.surf, (x0 - pview.w, 0))
	def alive(self):
		return True
