import pygame, math, random
from collections import Counter
from . import control, view, grid, state, settings, hud, generate, quest, graphics
from . import pview, ptext
from .pview import T



def init():
	global building, selected
	building = None
	selected = None
#	quest.inithard()
#	generate.tutorial1()
#	generate.tutorial2()
#	generate.tutorial3()
#	generate.tutorial4()
#	generate.tutorial5()
	generate.phase1()
	generate.phase2()
#	generate.phase3()
#	generate.revealto(30)
#	generate.ezphase1()
#	generate.ezphase2()
#	generate.ezphase3()
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
	if building is not None and "remove" in control.kdowns:
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
			selected = None
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
	quest.think(dt)


def draw():
	graphics.drawground()
	pygame.draw.circle(pview.screen, (255, 200, 128), control.posD, 3)

	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	if False:
		for pH in state.visible:
			if not state.isfree(pH): continue
			pD = view.DconvertG(grid.GconvertH(pH))
			alpha = 0.4 if pH == pHcursor else 0.12
			xH, yH = pH
			ptext.draw(f"{xH},{yH}", center = pD, alpha = alpha,
				fontsize = view.DscaleG(0.6), owidth = 2)
	if building is not None:
		for nextpH in building.nexts():
			graphics.outlineH(nextpH)

	for rock in state.rocks:
		rock.draw(glow = rock is selected)
	for tube in state.tubes:
		tube.draw(glow = tube is selected)
	for planet in state.planets:
		planet.draw(glow = planet is selected)
#		graphics.outlineH(planet.pH)
	if building is not None:
		building.draw(glow = True)
	graphics.renderqueue()

	graphics.drawsand()

	hud.draw()

	marquee = quest.marquee()
	if marquee:
		ptext.draw(marquee, width = T(800), midbottom = T(640, 690),
			fontsize = T(40), shade = 1, owidth = 1)

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



