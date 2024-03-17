import pygame
from . import control, view, grid, state
from . import pview, ptext


def init():
	global path
	path = None
	state.addplanet((0, 0))
	state.addplanet((4, -1))
	state.addplanet((-3, -2))
	state.addplanet((-2, 5))
	

def think(dt):
	global path
	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	if control.click:
		if pHcursor in state.planets and path is None:
			path = state.Path(pHcursor)
		if path is not None and path.cango(pHcursor):
			path.add(pHcursor)
	if control.rclick:
		if path is not None:
			state.paths.append(path)
			path = None

def draw():
	pview.fill((0, 0, 12))
	pygame.draw.circle(pview.screen, (255, 200, 128), control.posD, 3)

	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	for xH, yH in state.free:
		pD = view.DconvertG(grid.GconvertH((xH, yH)))
		alpha = 0.4 if (xH, yH) == pHcursor else 0.12
		ptext.draw(f"{xH},{yH}", center = pD, alpha = alpha, fontsize = 40, owidth = 2)

	for planetH in state.planets:
		pD = view.DconvertH(planetH)
		pygame.draw.circle(pview.screen, (0, 160, 160), pD, view.DscaleG(0.4))

	for p in state.paths:
		p.draw()
	if path is not None:
		path.draw(glow = True)

	pygame.display.flip()



