import pygame, math, random
from collections import Counter
from . import control, view, grid, state
from . import pview, ptext
from .pview import T


def init():
	global building, selected
	building = None
	selected = None
	state.addplanet((0, 0), has = {"R": 1, "O": 1, "Y": 1})
	for j in range(1, 100):
		pG = math.CS(j * math.phyllo, r = 2 * math.sqrt(j))
		pH = grid.HnearestG(pG)
		ncolor = int(math.interp(j, 1, 3, 40, 6))
		if j < 10:
			nhas, nneeds = 1, 1
		elif j < 30:
			nhas, nneeds = random.choice([[1, 2], [2, 1]])
		elif j < 60:
			nhas, nneeds = 2, 2
		else:
			nhas, nneeds = random.choice([[2, 3], [3, 2]])
		state.addrandomplanet(pH, ncolor, nhas, nneeds)

	for pH in state.board:
		if state.objat(pH) is None and random.random() < 0.2:
			state.addrock(pH)
		
#	state.addplanet((4, -1), needs = {"A": 1}, has = {"B": 1})
#	state.addplanet((-3, -2), needs = {"A": 1, "B": 1})
#	state.addplanet((-2, 5))
	state.resolvenetwork()

def think(dt):
	global building, selected
	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	if control.mclick:
		if state.planetat(pHcursor) and building is None:
			building = state.Tube(pHcursor)
			selected = None
	if control.click:
		if building is not None:
			if building.cango(pHcursor):
				building.add(pHcursor)
			elif state.planetat(pHcursor):
				building.add(pHcursor)
				state.addtube(building)
				building = None
		else:
			selected = state.objat(pHcursor)
	if control.rclick:
		building = None
	if isinstance(selected, state.Tube):
		if pygame.K_TAB in control.kdowns:
			selected.flip()
		if pygame.K_LSHIFT in control.kdowns:
			selected.togglecarry()
	dx = (control.kpressed["right"] - control.kpressed["left"]) * dt
	dy = (control.kpressed["up"] - control.kpressed["down"]) * dt
	view.scoot(dx, dy)


def draw():
	pview.fill((0, 0, 12))
	pygame.draw.circle(pview.screen, (255, 200, 128), control.posD, 3)

	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	if False:
		for (xH, yH), obj in state.board.items():
			if obj is not None: continue
			pD = view.DconvertG(grid.GconvertH((xH, yH)))
			alpha = 0.4 if (xH, yH) == pHcursor else 0.12
			ptext.draw(f"{xH},{yH}", center = pD, alpha = alpha,
				fontsize = view.DscaleG(0.6), owidth = 2)

	for rock in state.rocks:
		rock.draw(glow = rock is selected)
	for tube in state.tubes:
		tube.draw(glow = tube is selected)
	for planet in state.planets:
		planet.draw(glow = planet is selected)
	if building is not None:
		building.draw(glow = True)

	lines = [
		"Tab: switch selected tube flow",
		"Shift: switch selected tube item",
		"Left click: select planet or tube, continue tube",
		"Middle click: start tube at planet",
		"Right click: cancel tube",
	]
	if selected is not None:
		lines = selected.info() + lines
	ptext.draw("\n".join(lines), bottomright = pview.bottomright, fontsize = T(25),
		owidth = 1)



