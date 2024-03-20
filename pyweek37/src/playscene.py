import pygame, math, random
from collections import Counter
from functools import cache
from . import control, view, grid, state, settings, hud
from . import pview, ptext
from .pview import T


colorcosts = [1, 1, 1, 2, 2, 3]

@cache
def colorsets(cost, j0 = 0):
	if cost == 0:
		return [[]]
	if j0 >= len(colorcosts):
		return []
	ret = list(colorsets(cost, j0 + 1))
	if colorcosts[j0] <= cost:
		ret += [[j0] + cset for cset in colorsets(cost - colorcosts[j0], j0 + 1)]
	return ret

def randomplanet(hasvalue, needsvalue, *seed):
	for j in range(10000):
		has = math.fuzzchoice(colorsets(hasvalue), j, 101, *seed)
		needs = math.fuzzchoice(colorsets(needsvalue), j, 102, *seed)
		if not(set(has) & set(needs)):
			return [
				{ settings.colors[x]: 1 for x in has },
				{ settings.colors[x]: 1 for x in needs },
			]

def init():
	global building, selected
	building = None
	selected = None
	state.addplanet((0, 1), has = {"R": 1 })
	state.addplanet((1, -1), has = {"O": 1 })
	state.addplanet((-1, 0), has = {"Y": 1 })
	for j in range(4, 100):
		pG = math.CS(j * math.phyllo, r = 1.5 * math.sqrt(j))
		pH = grid.HnearestG(pG)
		hasvalue = int(math.interp(j, 1, 1, 60, 4))
		needsvalue = int(math.interp(j, 1, 1, 80, 4))
#		state.addrandomplanet(pH, ncolor, nhas, nneeds)
		has, needs = randomplanet(hasvalue, needsvalue, j)
		state.addplanet(pH, has = has, needs = needs)

	for pH in state.board:
		if state.objat(pH) is None and not any(state.planetat(pHadj) for pHadj in grid.HadjsH(pH)):
			if math.fuzz(1, *pH) < 0.35:
				state.addrock(pH)
	state.resolvenetwork()
	hud.init()

def think(dt):
	global building, selected
	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	if control.click:
		if building is not None:
			building.tryclick(pHcursor)
			if building.built:
				state.addtube(building)
				building = None
		else:
			selected = state.objat(pHcursor)
	if control.mclick:
		if state.planetat(pHcursor) and building is None:
			building = state.Tube(pHcursor)
			selected = None
	if control.dragfrom is not None and building is None:
		dragfromH = grid.HnearestG(view.GconvertD(control.dragfrom))
		if state.planetat(dragfromH):
			building = state.Tube(dragfromH)
			selected = None
	if any(control.dragD) and building is not None:
		building.trydrag(pHcursor)
		if building.built:
			state.addtube(building)
			building = None
	if control.rclick:
		building = None
		selected = None
	if isinstance(selected, state.Tube):
		if pygame.K_TAB in control.kdowns:
			selected.flip()
		if pygame.K_LSHIFT in control.kdowns:
			selected.togglecarry()
		if "remove" in control.kdowns:
			state.removetube(selected)
	dx = 600 * (control.kpressed["right"] - control.kpressed["left"]) * dt
	dy = 600 * (control.kpressed["down"] - control.kpressed["up"]) * dt
	view.scootD(dx, dy)
	view.scootD(-control.mdragD[0], -control.mdragD[1])
	view.zoom(control.dwheel, control.posD)
	for tube in state.tubes:
		tube.think(dt)
	for planet in state.planets:
		planet.think(dt)
	hud.think(dt)


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
	if building is not None:
		for nextpH in building.nexts():
			pDs = [view.DconvertG(pG) for pG in grid.GoutlineH(nextpH)]
			pygame.draw.lines(pview.screen, (0, 255, 255), True, pDs, 1)

	for rock in state.rocks:
		rock.draw(glow = rock is selected)
	for tube in state.tubes:
		tube.draw(glow = tube is selected)
	for planet in state.planets:
		planet.draw(glow = planet is selected)
	if building is not None:
		building.draw(glow = True)

	hud.draw()

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



