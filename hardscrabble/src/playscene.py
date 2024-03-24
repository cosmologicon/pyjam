import pygame, math, random
from collections import Counter
from functools import cache
from . import control, view, grid, state, settings, hud, generate, quest, graphics, sound
from . import pview, ptext
from .pview import T



@cache
def symbolsparks(pH, symbol):
	img = graphics.drawsymbol(symbol)
	w, h = img.get_size()
	sparks = []
	for j in range(200):
		x = math.fuzzrange(-1, 1, 2703, j, *pH)
		y = math.fuzzrange(-1, 1, 2704, j ,*pH)
		px = int(math.interp(x, -1, 0, 1, w - 1))
		py = int(math.interp(y, 1, 0, -1, h - 1))
		if img.get_at((px, py))[3] > 0:
			sparks.append((x, y))
	return sparks

class Firework:
	def __init__(self):
		self.nextwork = {}
		self.t = 0
		self.works = []
	def think(self, dt):
		self.t += dt
		for planet in state.planets:
			twork = math.fuzzrange(10, 20, 2700, *planet.pH)
			t0 = math.fuzzrange(0, twork, 2701, *planet.pH)
			if planet.pH not in self.nextwork:
				self.nextwork[planet.pH] = t0
			t = self.nextwork[planet.pH]
			if planet.supplied and planet.supply and self.t > t:
				symbol = math.fuzzchoice(planet.supply, 2702, t)
				work = t, planet.pH, symbol
				self.nextwork[planet.pH] += twork
				self.works.append(work)
		self.works = [(t, pH, symbol) for t, pH, symbol in self.works if t < self.t + 10]
	def drawpoint(self, pH, dxG, zG, color, sizeG):
		xG, yG = grid.GconvertH(pH)
		pD = view.DconvertG((xG + dxG, yG), zG)
		pygame.draw.circle(pview.screen, color, pD, view.DscaleG(sizeG))
	def draw(self):
		for t, pH, symbol in self.works:
			dt = self.t - t
			if dt < 1:
				color = math.imix((50, 50, 50), (255, 255, 255), math.fuzz(dt, *pH))
				h = math.mix(0.4, 5, (dt / 1) ** 0.4)
				self.drawpoint(pH, 0, h, color, 0.12)
			elif dt < 3:
				r = 2.5 * math.interp(dt, 1, 0, 3, 1) ** 0.5
				h = 5 - 0.5 * (dt - 1.5) ** 2
				color = settings.getcolor(symbol)
				color = math.imix(color, (255, 255, 255), 0.5)
				sparks = symbolsparks(pH, symbol)
				nsparks = int(math.interp(dt, 2.5, 1, 3, 0) * len(sparks))
				for dx, dz in sparks[:nsparks]:
					self.drawpoint(pH, r * dx, h + r * dz * 1.4, color, 0.04)


def init():
	global building, marquee0, malpha, firework
	building = None
	state.load()
	if state.level == "tutorial":
		sound.playmusic("notasitseems")
	else:
		sound.playmusic("entertheparty")
#	state.init()
#	generate.medphase1()
#	generate.medphase2()
#	generate.medphase3()
	control.init()
	control.selected = None
	marquee0 = None
	malpha = 0
	hud.init()
	firework = Firework()
	

def think(dt):
	global building, marquee0, malpha, twin, fireworks
	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	hud.think(dt)
	if control.click:
		if building is not None:
			if len(building.pHs) == 1 and state.planetat(pHcursor) not in [None, building.supplier]:
				building = state.Tube(pHcursor)
				sound.play("start")
			else:
				dlen = building.tryclick(pHcursor)
				if not building.supplier:
					sound.play("cancel")
					building = None
				elif building.built:
					state.addtube(building)
					building = None
				elif dlen > 0:
					sound.play("buildup")
				elif dlen < 0:
					sound.play("builddown")
				else:
					sound.play("no")
		else:
			control.selected = state.objat(pHcursor)
			if isinstance(control.selected, state.Planet):
				building = state.Tube(pHcursor)
				control.selected = None
				sound.play("start")
			elif isinstance(control.selected, state.Tube):
#				sound.play("select")
				sound.play("click")
			else:
				control.selected = None
				sound.play("click")
			
	if control.dragfrom is not None and building is None and control.self.current == 1:
		dragfromH = grid.HnearestG(view.GconvertD(control.dragfrom))
		if state.planetat(dragfromH):
			building = state.Tube(dragfromH)
			sound.play("start")
			control.selected = None
	if any(control.dragD) and building is not None:
		dlen = building.trydrag(pHcursor)
		if building.built:
#			sound.play("complete")
			sound.play("buildup")
			state.addtube(building)
			building = None
		elif dlen > 0:
			sound.play("buildup")
		elif dlen < 0:
			sound.play("builddown")
		
	if building is not None and "remove" in control.kdowns:
		sound.play("cancel")
		building = None
	if control.rclick:
		building = None
		control.selected = None

	if pygame.K_TAB in control.kdowns:
		settings.expandinfo = not settings.expandinfo
		settings.save()

	if isinstance(control.selected, state.Tube):
		if "remove" in control.kdowns:
			state.removetube(control.selected)
			control.selected = None
	dx = T(600 * (control.kpressed["right"] - control.kpressed["left"]) * dt)
	dy = T(600 * (control.kpressed["down"] - control.kpressed["up"]) * dt)
	view.scootD((dx - control.rdragD[0], dy - control.rdragD[1]))
	if control.dwheel > 0:
		view.zoomstep(1, control.posD)
	if "zoomin" in control.kdowns:
		view.zoomstep(1)
	if control.dwheel < 0:
		view.zoomstep(-1, control.posD)
	if "zoomout" in control.kdowns:
		view.zoomstep(-1)
	if settings.DEBUG and "cheat" in control.kdowns:
		if building and len(building.pHs) == 1:
			building.supplier.cheat()

	for tube in state.tubes:
		tube.think(dt)
	for planet in state.planets:
		planet.think(dt)
	quest.think(dt)
	marquee = quest.marquee()
	alpha = 1 if marquee == marquee0 is not None else 0
	malpha = math.approach(malpha, alpha, 5 * dt)
	if malpha == 0:
		marquee0 = marquee
	if quest.quests[0].step == 10:
		firework.think(dt)


def draw():
	graphics.drawground()
#	pygame.draw.circle(pview.screen, (255, 200, 128), control.posD, 3)

	pGcursor = view.GconvertD(control.posD)
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
		color = (200, 200, 255)
		d = math.interp(math.log(view.DscaleG(1)), math.log(20), 0.1, math.log(300), 1)
		color = math.imix((50, 40, 30), color, d)
		tiles = [pH for pH in state.visible if math.distance(grid.GconvertH(pH), pGcursor) < 3]
		for pG0, pG1 in grid.GgridoutlineH(tiles):
			pygame.draw.aaline(pview.screen, color, view.DconvertG(pG0), view.DconvertG(pG1))
		for nextpH in building.nexts():
			graphics.targetH(nextpH)
#			graphics.outlineH(nextpH)

	dmax = max(grid.normH(pH) for pH in state.visible)
	for pH in state.board:
		if pH not in state.visible and grid.normH(pH) < dmax + 2:
#			graphics.drawcircleH(pH, (255, 255, 255), 0.4)
			graphics.drawcloudatH(pH)
	graphics.fog(dmax)

	for rock in state.rocks:
		rock.draw()
	for tube in state.tubes:
		tube.draw()
	for planet in state.planets:
		planet.draw()
	graphics.renderqueue()

	if building is not None:
		building.drawglow()
	if control.selected is not None:
		control.selected.drawglow()

	for tube in state.tubes:
		tube.drawcarry()
	graphics.renderqueue()
	for planet in state.planets:
		planet.drawbubbles()
	graphics.renderqueue()

	firework.draw()

	graphics.drawsand()

	hud.draw()

	if malpha and marquee0 is not None:
		ptext.draw(marquee0, width = T(800), midbottom = T(640, 690),
			fontname = "OdibeeSans",
			fontsize = T(40), shade = 1, owidth = 1, alpha = malpha)

	if settings.expandinfo:
		lines = [
			"Tab: hide controls",
			"Left click or drag: build conduit",
			"Right click: cancel build",
			"Right drag, WASD, arrow keys: pan",
			"Scroll wheel or 1 and 2 keys: zoom",
			"Backspace: delete selected conduit",
			"F10: change resolution",
			"F11: toggle fullscreen",
			"F12: screenshot",
#			f"{view.VscaleG}, {view.xG0}, {view.yG0}",
		]
	else:
		lines = ["Tab: show controls"]
#	pygame.draw.circle(pview.screen, (255, 200, 100), view.DconvertG((view.xG0, view.yG0)), 3)
#	pygame.draw.circle(pview.screen, (100, 255, 100), view.DconvertG((0, 0)), 3)
#	pygame.draw.circle(pview.screen, (100, 255, 100), view.DconvertG((0, 1)), 3)
#	pygame.draw.circle(pview.screen, (100, 255, 100), view.DconvertG((1, 1)), 3)
	if settings.DEBUG and control.selected is not None:
#		lines += control.selected.info()
		lines += control.selected.supplier.info()
	ptext.draw("\n".join(lines), topright = T(1262, 10), fontsize = T(19),
		fontname = "RussoOne", owidth = 0.5, color = (200, 200, 255), shade = 0.5)



