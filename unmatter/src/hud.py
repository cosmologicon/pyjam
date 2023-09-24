import pygame
from . import ptext, pview, state, settings, progress, quest
from .pview import T


def draw():
	ptext.draw("HULL", topleft = T(10, 0), fontsize = T(30), color = (120, 180, 180), shade = 1)
	rect = pygame.Rect(T(114, 8, 12, 22))
	for j in range(progress.getmaxhp()):
		width = 0 if j < state.hp else T(2)
		pygame.draw.rect(pview.screen, (120, 180, 180), rect, width)
		rect.x += T(15)

	if progress.getmaxenergy():
		ptext.draw("CHARGE", topleft = T(10, 30), fontsize = T(30), color = (180, 180, 120), shade = 1)
		rect = pygame.Rect(T(164, 8, 12, 22))
		rect.y += T(30)
		for j in range(progress.getmaxenergy()):
			width = 0 if j < state.energy else T(2)
			pygame.draw.rect(pview.screen, (160, 160, 100), rect, width)
			rect.x += T(15)

	if state.you.cageunlocked():
		ptext.draw(f"XP {state.xp}", topleft = T(10, 60), fontsize = T(30), color = (0, 0, 0), owidth = 1, ocolor = "gray")
	
	infos = []
	if state.you.cageunlocked():
		infos.append("gravnet")
	if False:
		if state.you.beamunlocked():
			infos.append("beam")
	srect = pygame.Rect(T(10, 106, 120, 30))
	for j, info in enumerate(infos):
		rect = pygame.Rect(0, 0, srect.w, srect.h)
		surf = pygame.Surface(rect.size).convert_alpha()
		surf.fill((0, 0, 0, 0))
		color = (100, 255, 255, 50)
		pygame.draw.rect(surf, color, rect, T(4))
		rect.w = pview.I(rect.w * state.charge[info])
		if rect.w:
			pygame.draw.rect(surf, color, rect)
		pview.screen.blit(surf, srect)
		color = (100, 255, 255) if state.charge[info] == 1 else (40, 100, 100)
		ptext.draw(info.upper(), center = srect.center, fontsize = T(20),
			owidth = 0.5, color = color, alpha = 0.6)
		srect.y -= 50

def drawcontrols():
	text = "\n".join(quest.getcontrolinfo())
	if text:
		ptext.draw(text, bottomleft = T(10, 710), fontsize = T(16), color = (200, 255, 255), shade = 1)
	
