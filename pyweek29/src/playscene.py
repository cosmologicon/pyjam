import pygame, statistics, math
from . import pview, view, thing, state, settings, control, level, progress, sound, ptext
from . import scene, dialogscene
from . import draw as D
from .pview import T

class self:
	pass

def init():
	level.load()
	self.alpha = 1
	self.losing = False
	self.lepdtf = 1
	t0 = pygame.time.get_ticks()
	self.killed = False
	self.tfly = 0
	self.ending = False
	

def control(keys):
	if "forfeit" in keys:
		self.losing = True
	if not state.winning() and not self.losing:
		state.you.control(keys)

def think(dt):
	self.tfly += dt
	if not self.killed:
		D.finishkill()
		self.killed = True

	if state.winning() and not self.ending:
		self.ending = True
		self.tfly = 0
	if self.losing and not self.ending:
		self.ending = True
		self.tfly = 10

	if self.ending:
		kdowns = set()
		if self.tfly >= 2:
			self.alpha = math.approach(self.alpha, 1, 4 * dt)
			if self.alpha == 1:
				scene.pop()
				if state.winning():
					progress.beat(progress.at)
					scene.push(dialogscene, "%s-post" % progress.at)
				
	else:
		self.alpha = math.approach(self.alpha, 0, 4 * dt)
	state.you.think(dt)
	self.lepdtf = math.approach(self.lepdtf, (0.1 if state.you.state == "jumping" else 1), 4 * dt)
	for lep in state.leps:
		lep.think(dt * self.lepdtf)
	for lep in state.goals:
		lep.think(dt * self.lepdtf)
	if state.guided is not None:
		state.guided.think(dt * self.lepdtf)
	view.think(dt)

def draw():
	D.background("lake.jpg", (160, 160, 160))
	gridlines = [((x, 0), (x, state.h)) for x in range(0, state.w + 1)]
	gridlines += [((0, y), (state.w, y)) for y in range(1, state.h + 1)]
	if False:
		if state.you.state == "jumping":
			for p0, p1 in gridlines:
				pygame.draw.line(pview.screen, (50, 50, 140),
					view.worldtoscreen(p0), view.worldtoscreen(p1), T(1))
	state.you.draw()
	for lep in state.goals:
		lep.draw()
	if state.guided is not None:
		state.guided.draw()
	(xmin, xmax), (ymin, ymax) = view.visiblerange()
	for lep in state.leps:
		if xmin <= lep.x <= xmax and ymin <= lep.y <= ymax:
			lep.draw()
	if state.guided:
		state.guided.draw()

	tiptext = ""
	if progress.at == "tutorial1":
		tiptext = "Tap Arrow keys or WASD to jump"
	if progress.at == "tutorial2":
		tiptext = "Tap two directions at one to jump diagonal"
	if progress.at == "tutorial4":
		tiptext = "Sparkling butterflies can be moved\nTap Space or Enter to guide and release"
	
	if tiptext:
		ptext.draw(tiptext, fontname = "ChangaOne", color = (255, 220, 200), fontsize = T(44),
			midbottom = T(view.rrect.left / 2, 680),  shade = 1, owidth = 0.5, shadow = (1, 1))

	# Right panel
#	pview.fill((80, 80, 100, 220), T(view.rrect))
	D.panel()
	for p0, p1 in gridlines:
		pygame.draw.line(pview.screen, (100, 60, 120), view.worldtomap(p0), view.worldtomap(p1), T(1))
	state.you.drawmap()
	for lep in state.leps:
		lep.drawmap()
	for lep in state.leps:
		lep.drawarrowsmap()
	mcenter0 = view.rrect.centerx, 120
	mcenter = T(mcenter0)
	D.drawimg("guiding", mcenter, 1000 * pview.f, owidth = 2)
	if state.guided:
		state.guided.drawguided(mcenter0)
	ptext.draw("Guiding", center = (mcenter[0], 20), fontsize = T(30), fontname = "ChangaOne",
		color = "white", owidth = 1.5, shade = 1)
	if False:
		pygame.draw.circle(pview.screen, (255, 200, 80), mcenter, T(50), T(2))
		pygame.draw.circle(pview.screen, (255, 200, 80), mcenter, T(50 * state.you.jumpmeter()))
		for j in range(state.maxleaps):
			pos = T(view.rrect.centerx + 60 * (-(state.maxleaps - 1) / 2 + j), 160)
			if j < state.leaps:
				pygame.draw.circle(pview.screen, (255, 200, 80), pos, T(24))
			else:
				pygame.draw.circle(pview.screen, (255, 200, 80), pos, T(24), T(2))

	controls = "\n".join([
		"Space: guide/release",
		"Backspace: exit level",
	])
	ptext.draw(controls, fontname = "ChangaOne", color = (255, 220, 200), fontsize = T(18),
		bottomright = T(1270, 710),  shade = 1, owidth = 0.5, shadow = (1, 1))

	if 0 < self.tfly < 2:
		dt = (self.tfly / 2 - 0.5) * 2
		x = 500 - 2400 * dt + 2300 * math.clamp(dt, -0.6, 0.6)
		ptext.draw(level.currentname(), fontname = "CarterOne",
			color = (200, 200, 255), fontsize = T(100),
			center = T(x, 300), shade = 1, owidth = 0.2, shadow = (1, 1))
		if state.winning():
			text = "Stage Complete"
		elif self.losing:
			text = "Stage Failed"
		else:
			text = ""
		if text:
			x = 700 + 2400 * dt - 2300 * math.clamp(dt, -0.6, 0.6)
			ptext.draw(text, fontname = "CarterOne",
				color = (200, 200, 255), fontsize = T(100),
				center = T(x, 500), shade = 1, owidth = 0.2, shadow = (1, 1))


	if self.alpha:
		pview.fill((255, 255, 255, int(255 * self.alpha)))


