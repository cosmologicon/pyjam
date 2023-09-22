import random, math, pygame
from . import settings, state, thing, view, graphics, sector, quest, perform, progress
from . import pview, ptext
from .pview import T


def init():
	progress.init()

def resume():
	state.you.A = 0
	state.you.leave(state.at)
	state.at = None


def think(dt, kdowns = [], kpressed = [0] * 128, mpos = (0, 0), mdowns = set()):
	perform.start("think")
	state.you.control(kdowns, kpressed)
	perform.start("statethink")
	state.you.think(dt)
	for pulse in state.pulses:
		pulse.think(dt)
	for spawner in state.spawners:
		spawner.think(dt)
	for DM in state.DMs:
		DM.think(dt)
	for tracer in state.tracers:
		tracer.think(dt)
	for shot in state.shots:
		shot.think(dt)
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
		view.VscaleG = 40
	for spot in state.spots:
		if thing.overlaps(state.you, spot):
			from . import scene, homescene
			if spot is state.home:
				state.at = spot
				scene.current = homescene
				homescene.init()
	perform.stop("think")


def draw():
	pview.fill((0, 0, 0))
	perform.start("drawnebula")
	graphics.drawnebula()
	perform.stop("drawnebula")
	perform.start("drawstars")
	graphics.drawstars()
	perform.stop("drawstars")

	perform.start("drawstate")
	for pulse in state.pulses:
		pulse.draw()
	for DM in state.DMs:
		DM.draw()
	for tracer in state.tracers:
		tracer.draw()
	for shot in state.shots:
		shot.draw()
	for spot in state.spots:
		spot.draw()
	state.you.draw()
	if settings.drawbox:
		for DM in state.DMs:
			DM.drawbox()
		for spot in state.spots:
			spot.drawbox()
		state.you.drawbox()
	perform.stop("drawstate")
	drawminimap()
#	drawmap()
	text = quest.info()
	if text:
		ptext.draw(text, midbottom = T(640, 710), fontsize = T(50), width = T(800), owidth = 1,
			color = "#ff7fff", shade = 1)
	quest.marquee.draw()
	drawHUD()


def drawmap():
	perform.start("drawmap")
	mradius = 500
	mrect = T(pygame.Rect(0, 0, 640, 640))
	def MconvertG(pos):
		x, y = pos
		return pview.T(640 + 320 / mradius * x, 360 - 320 / mradius * y)
	mrect.center = pview.center
	pview.screen.fill((10, 10, 10), mrect)
	for DM in state.DMs:
		pM = MconvertG(DM.pos)
		pygame.draw.circle(pview.screen, (0, 0, 0), pM, T(3))
		pygame.draw.circle(pview.screen, (0, 255, 255), pM, T(3), T(1))
	pygame.draw.circle(pview.screen, (255, 0, 0), MconvertG(state.you.pos), T(5))
	perform.stop("drawmap")


def drawminimap():
	perform.start("drawminimap")
	mradius = 50
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
		pygame.draw.circle(img, color, pM, T(k * rV))
		if ocolor is not None:
			pygame.draw.circle(img, ocolor, pM, T(k * rV), k)

	for DM in state.DMs:
		if DM.found:
			drawcircleG(DM.pos, 3, (0, 0, 0), (0, 200, 200))
	for spot in state.spots:
		drawcircleG(spot.pos, 8, (0, 0, 0), (0, 200, 200))
	drawcircleG(state.you.pos, 4, (60, 30, 0), (120, 60, 0))
	if k != 1:
		img = pygame.transform.smoothscale(img, (2 * s, 2 * s))
	rect = img.get_rect(bottomright = T(1270, 710))
	pview.screen.blit(img, rect)
	pygame.draw.rect(pview.screen, (60, 120, 120), rect, 1)
	perform.stop("drawminimap")


def drawHUD():
	infos = []
	if state.you.cageunlocked():
		infos.append("gravnet")
	if state.you.beamunlocked():
		infos.append("beam")
	srect = pygame.Rect(T(15, 620, 160, 40))
	for j, info in enumerate(infos):
		rect = pygame.Rect(0, 0, srect.w, srect.h)
		surf = pygame.Surface(rect.size).convert_alpha()
		surf.fill((0, 0, 0, 0))
		color = (100, 100, 255, 50)
		pygame.draw.rect(surf, color, rect, T(4))
		rect.w = pview.I(rect.w * state.charge[info])
		if rect.w:
			pygame.draw.rect(surf, color, rect)
		pview.screen.blit(surf, srect)
		ptext.draw(info.upper(), center = srect.center, fontsize = T(40), owidth = 0.5, color = (100, 100, 255), alpha = 0.5)
		srect.y -= 50

	text = f"XP: {state.xp}"
	ptext.draw(text, bottomleft = T(15, 710), fontsize = T(50), color = (200, 255, 255), shade = 1)
	


