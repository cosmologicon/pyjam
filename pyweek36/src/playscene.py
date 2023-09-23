import random, math, pygame
from collections import defaultdict
from . import settings, state, thing, view, graphics, sector, quest, perform, progress, hud, sound
from . import pview, ptext
from .pview import T


def init():
	progress.init()
	progress.cheat()
	think(0)
	return
	for j, DM in enumerate(state.DMs):
		DM.found = math.fuzzflip(j, 123)
	for j, spot in enumerate(state.spots):
		spot.unlocked = math.fuzzflip(j, 234)

def resume():
	state.you.A = 0
	state.you.leave(state.at)
	state.at = None


def think(dt, kdowns = [], kpressed = defaultdict(bool), mpos = (0, 0), mdowns = set()):
	perform.start("think")
	state.you.control(kdowns, kpressed, mdowns)
	state.showmap = any(kpressed[key] for key in settings.keys["map"])
	perform.start("statethink")
	state.you.think(dt)
	for pulse in state.pulses:
		pulse.think(dt)
	for spawner in state.spawners:
		spawner.think(dt)
	state.DMtracker.think(dt)
	for tracer in state.tracers:
		tracer.think(dt)
	for shot in state.shots:
		shot.think(dt)
	for spot in state.spots:
		spot.think(dt)
	perform.stop("statethink")
	state.pulses = [pulse for pulse in state.pulses if pulse.alive]
	state.tracers = [tracer for tracer in state.tracers if tracer.alive]
	state.shots = [shot for shot in state.shots if shot.alive]
	quest.think(dt)
	quest.marquee.think(dt)
	if math.hypot(*state.you.pos) < 0:
		view.xG0, view.yG0 = math.mix((0, 0), state.you.pos, 0.5)
		view.VscaleG = math.interp(math.hypot(*state.you.pos), 0, 100, 10, 40)
	else:
		view.xG0, view.yG0 = state.you.pos
		view.VscaleG = 50
	for spot in state.spots:
		if thing.overlaps(state.you, spot):
			from . import scene, homescene
			if spot is state.home:
				state.at = spot
				scene.current = homescene
				homescene.init()
				sound.play("arrive")

	perform.stop("think")
	if state.techlevel["return"] > 0 and any(key in kdowns for key in settings.keys["return"]):
		from . import scene, homescene
		state.you.pos = state.home.pos
		state.at = state.home
		sound.play("return")
		scene.current = homescene
		homescene.init()
		


def draw():
	pview.fill((0, 0, 0))
	for pulse in state.pulses:
		pulse.draw()
	state.you.drawglow()
	perform.start("drawnebula")
	graphics.drawnebula()
	perform.stop("drawnebula")
	perform.start("drawstars")
	graphics.drawstars()
	perform.stop("drawstars")

	perform.start("drawstate")
	state.you.drawbeam()
	for DM in state.DMtracker.active:
		DM.draw()
	for tracer in state.tracers:
		tracer.draw()
	for shot in state.shots:
		shot.draw()
	for spot in state.spots:
		spot.draw()
	state.you.draw()
	if settings.drawbox:
		for DM in state.DMtracker.active:
			DM.drawbox()
		for spot in state.spots:
			spot.drawbox()
		state.you.drawbox()
	perform.stop("drawstate")
	drawminimap()
	if state.techlevel["map"] > 0 and state.showmap:
		drawmap()
	text = quest.info()
	if text:
		ptext.draw(text, midbottom = T(640, 710), fontname = "JollyLodger", fontsize = T(50),
			width = T(700), owidth = 1, color = "#ff7fff", shade = 1)
	quest.marquee.draw()
	hud.draw()
	hud.drawcontrols()


def drawmap():
	perform.start("drawmap")
	flash = pygame.time.get_ticks() % 1000 > 500

	mradius = 1000
	s = 340
	k = 1
	img = pygame.Surface(T(2 * k * s, 2 * k * s)).convert_alpha()
	img.fill((0, 0, 0, 200))
	def MconvertG(pos):
		x, y = pos
		return T(k * s + k * s / mradius * x, k * s - k * s / mradius * y)

	def drawcircleG(posG, rV, color, ocolor=None):
		pM = MconvertG(posG)
		pygame.draw.circle(img, color, pM, T(k * rV))
		if ocolor is not None:
			pygame.draw.circle(img, ocolor, pM, T(k * rV), k)

	Dring = 100
	Nspoke = 8
	color = math.imix((0, 0, 0), (128, 255, 255), k / 4)
	for jring in range(1, 11):
		rG = Dring * jring
		rV = rG * s / mradius
		pygame.draw.circle(img, color, MconvertG((0, 0)), T(k * rV), 1)
	for jspoke in range(48):
		A = jspoke / Nspoke * math.tau / 6
		jring = Nspoke
		while jring > 1 and jspoke % 2 == 0:
			jring /= 2
			jspoke /= 2
		r0, r1 = jring * Dring, 10 * Dring
		pygame.draw.line(img, color, MconvertG(math.CS(A, r0)), MconvertG(math.CS(A, r1)), 1)

	for DM in state.DMs:
		color = DM.mapcolor()
		if color is not None:
			drawcircleG(DM.pos, 1, color)
	for spot in state.spots:
		if spot.unlocked:
			drawcircleG(spot.pos, 5, (0, 0, 0), (0, 200, 200))
			if flash:
				ptext.draw(f"{spot.nunfound()}", center = MconvertG(spot.pos), fontsize = T(25 * k), owidth = 1, surf=img)
	if not flash:
		drawcircleG(state.you.pos, 6, (200, 100, 100), (255, 128, 128))
	if k != 1:
		img = pygame.transform.smoothscale(img, (2 * s, 2 * s))
	rect = img.get_rect(center = pview.center)
	pview.screen.blit(img, rect)
	pygame.draw.rect(pview.screen, (60, 120, 120), rect, 1)
	perform.stop("drawmap")


def drawminimap():
	perform.start("drawminimap")
	mradius = settings.minimapradius
	s = 120
	k = 2
	img = pygame.Surface(T(2 * k * s, 2 * k * s)).convert_alpha()
	img.fill((0, 0, 0, 200))
	x0, y0 = state.you.pos
	def MconvertG(pos):
		x, y = pos
		return T(k * s + k * s / mradius * (x - x0), k * s - k * s / mradius * (y - y0))
	D = thing.pdist((x0, y0), (0, 0))
	Dmin, Dmax = D - 1.5 * mradius, D + 1.5 * mradius
	Dring = 30
	jring1 = int(Dmax / Dring) + 1
	Nspoke = 1
	while Nspoke < jring1:
		Nspoke *= 2
	if Dmin < 0:
		jring0 = 1
		jspoke0, jspoke1 = 0, 6 * Nspoke
	else:
		jring0 = max(1, int(Dmin / Dring))
		Acenter = math.atan2(y0, x0)
		dA = 1.5 * mradius / Dmin
		jspoke0 = int((Acenter - dA) * 6 * Nspoke / math.tau)
		jspoke1 = int((Acenter + dA) * 6 * Nspoke / math.tau) + 1
	for jring in range(jring0, jring1):
		rG = Dring * jring
		rV = rG * s / mradius
		pygame.draw.circle(img, (60, 120, 120), MconvertG((0, 0)), T(k * rV), 1)
	for jspoke in range(jspoke0, jspoke1):
		A = jspoke / Nspoke * math.tau / 6
		jring = Nspoke
		while jring > 1 and jspoke % 2 == 0:
			jring /= 2
			jspoke /= 2
		r0, r1 = max(jring * Dring, Dmin), Dmax
		pygame.draw.line(img, (60, 120, 120), MconvertG(math.CS(A, r0)), MconvertG(math.CS(A, r1)), 1)

	def drawcircleG(posG, rV, color, ocolor=None):
		pM = MconvertG(posG)
		if color is not None:
			pygame.draw.circle(img, color, pM, T(k * rV))
		if ocolor is not None:
			pygame.draw.circle(img, ocolor, pM, T(k * rV), k)

	perform.start("drawminimapspots")
	for spot in state.spots:
		if spot.unlocked:
			drawcircleG(spot.pos, 8, (0, 0, 0), (0, 200, 200))
			rV = settings.countradius * s / mradius
			pygame.draw.circle(img, (30 * k, 15 * k, 0), MconvertG(spot.pos), T(k * rV), 1)
	perform.stop("drawminimapspots")
	perform.start("drawminimapDM")
	for DM in state.DMtracker.active:
		if DM.found:
			drawcircleG(DM.pos, 3, (0, 0, 0), (0, 200, 200))
	perform.stop("drawminimapDM")
	drawcircleG(state.you.pos, 4, (60, 30, 0), (120, 60, 0))
	if k != 1:
		img = pygame.transform.smoothscale(img, (2 * s, 2 * s))
	rect = img.get_rect(bottomright = T(1270, 710))
	pview.screen.blit(img, rect)
	pygame.draw.rect(pview.screen, (60, 120, 120), rect, 1)
	perform.stop("drawminimap")





