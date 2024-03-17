import pygame
from . import control, view, grid
from . import pview, ptext


def init():
	global path
	path = []

def think(dt):
	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	if control.click:
		if pHcursor not in path:
			path.append(pHcursor)

def draw():
	pview.fill((0, 0, 12))
	pygame.draw.circle(pview.screen, (255, 200, 128), control.posD, 3)

	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	for xH in range(-5, 6):
		for yH in range(-5, 6):
			if abs(xH + yH) > 5: continue
			pD = view.DconvertG(grid.GconvertH((xH, yH)))
			alpha = 0.4 if (xH, yH) == pHcursor else 0.12
			ptext.draw(f"{xH},{yH}", center = pD, alpha = alpha, fontsize = 40, owidth = 2)

	pDs = [view.DconvertG(grid.GconvertH(pH)) for pH in path]
	for pD in pDs:
		pygame.draw.circle(pview.screen, (0, 0, 100), pD, view.DscaleG(0.2), 1)
	if len(pDs) >= 2:
		pygame.draw.lines(pview.screen, (0, 50, 0), False, pDs, view.DscaleG(0.1))

	pygame.display.flip()



