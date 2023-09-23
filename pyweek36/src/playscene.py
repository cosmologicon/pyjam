import random, math, pygame
from collections import defaultdict
from functools import lru_cache
from . import settings, state, thing, view, graphics, sector, quest, perform, progress, hud, sound
from . import pview, ptext
from .pview import T

trespawn = 0


def init():
	progress.init()
#	progress.cheat()
	think(0)
	pygame.mouse.set_visible(False)
	sound.playmusic("floating-cities")
	if settings.qunlock:
		for j, DM in enumerate(state.DMs):
			if math.fuzzflip(j, 123):
				DM.find()
		for j, spot in enumerate(state.spots):
			spot.unlocked = math.fuzzflip(j, 234)


def resume():
	sound.playmusic("floating-cities")
	sound.play("leave")
	state.you.A = 0
	state.you.leave(state.at)
	state.at = None
	progress.save()
	progress.quicksave(force = True)
	pygame.mouse.set_visible(False)
	quest.marquee.append("GAME SAVED")
	think(0)


def think(dt, kdowns = [], kpressed = defaultdict(bool), mpos = (0, 0), mdowns = set()):
	perform.start("think")
	state.you.control(kdowns, kpressed, mdowns)
	state.showmap = any(kpressed[key] for key in settings.keys["map"])
	perform.start("statethink")
	state.you.think(dt)
	for pulse in state.pulses:
		pulse.think(dt)
	state.DMtracker.think(dt)
	for shot in state.shots:
		shot.think(dt)
	for spot in state.spots:
		spot.think(dt)
	perform.stop("statethink")
	state.pulses = [pulse for pulse in state.pulses if pulse.alive]
	state.shots = [shot for shot in state.shots if shot.alive]
	quest.think(dt)
	quest.marquee.think(dt)
	if math.hypot(*state.you.pos) < 0:
		view.xG0, view.yG0 = math.mix((0, 0), state.you.pos, 0.5)
		view.VscaleG = math.interp(math.hypot(*state.you.pos), 0, 100, 10, 40)
	else:
		view.xG0, view.yG0 = state.you.pos
		view.VscaleG = settings.viewscale
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
	progress.quicksave()
	global trespawn
	if state.hp <= 0:
		if trespawn == 0:
			sound.play("die")
		trespawn = math.approach(trespawn, 3, dt)
	else:
		trespawn = 0
	if trespawn == 3:
		from . import scene, homescene
		progress.loadlastsave()
		state.at = state.home
		scene.current = homescene
		homescene.init()
		sound.play("respawn")
		


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
			width = T(700), owidth = 1, color = "#7fffff", shade = 1)
	quest.marquee.draw()
	hud.draw()
	hud.drawcontrols()
	if quest.drawtitle():
		ocolor = "#cfffff"
		ptext.draw(settings.gamename, center = T(640, 140), fontname = "JollyLodger", fontsize = T(120),
			owidth = 0.2, color = "#333333", gcolor = "black", ocolor = ocolor, scolor = ocolor, shadow = (0.3, 0.3))
		text = "\n".join([
			"by Christopher Night",
			"music: Kevin Macleod (incompetech.com)",
			"graphics: pendleburyannette, WikiImages, MillionthVector",
			"fonts: Jovanny Lemonad, Font Diner",
		])
		ptext.draw(text, midtop = T(640, 540), fontsize = T(20), shade = 1, owidth = 0.5)

def drawmap():
	perform.start("drawmap")
	flash = pygame.time.get_ticks() % 1000 > 500

	mradius = settings.mapradius
	s = 340
	k = 1
	img = minimapimg(k, s)
	img.fill((0, 0, 0, 200))
	def MconvertG(pos):
		x, y = pos
		return T(k * s + k * s / mradius * x, k * s - k * s / mradius * y)

	def drawcircleG(posG, rV, color, ocolor=None):
		pM = MconvertG(posG)
		pygame.draw.circle(img, color, pM, T(k * rV))
		if ocolor is not None:
			pygame.draw.circle(img, ocolor, pM, T(k * rV), k)

	Dring = 50
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
			drawcircleG(DM.pos, max(1, DM.r), color)
	for spot in state.spots:
		if spot.unlocked:
			drawcircleG(spot.pos, 5, (0, 0, 0), (0, 200, 200))
			if flash:
				text = f"{spot.nunfound(countall=True)}"
				ptext.draw(text, center = MconvertG(spot.pos), fontsize = T(10 * k),
					color = (100, 255, 255), owidth = 1, surf=img)
	if not flash:
		drawcircleG(state.you.pos, 6, (80, 0, 0), (160, 0, 0))
	if k != 1:
		img = pygame.transform.smoothscale(img, (2 * s, 2 * s))
	rect = img.get_rect(center = pview.center)
	pview.screen.blit(img, rect)
	pygame.draw.rect(pview.screen, (60, 120, 120), rect, 1)
	perform.stop("drawmap")

	if trespawn:
		alpha = math.imix(0, 200, math.interp(trespawn, 0, 0, 1, 1))
		pview.fill((0, 0, 0, alpha))
		alpha = math.imix(0, 255, math.interp(trespawn, 0.5, 0, 1.5, 1))
		ptext.draw("LOADING LAST SAVE", fontsize = T(60), color = (200, 255, 255), owidth = 0.5, shade = 1,
			alpha = alpha)

@lru_cache(2)
def minimapimg(k, s):
	return pygame.Surface(T(2 * k * s, 2 * k * s)).convert_alpha()


def drawminimap():
	perform.start("drawminimap")
	perform.start("minimapsetup")
	mradius = settings.minimapradius
	s = T(120)
	k = 2
	img = minimapimg(k, s)
	img.fill((0, 0, 0, 200))
	x0, y0 = state.you.pos
	def MconvertG(pos):
		x, y = pos
		return T(k * s + k * s / mradius * (x - x0), k * s - k * s / mradius * (y - y0))
	perform.start("minimapgrid")
	D = thing.pdist((x0, y0), (0, 0))
	Dmin, Dmax = D - 1.5 * mradius, D + 1.5 * mradius
	Dring = 30
	jring1 = int(Dmax / Dring) + 1
	Nspoke = 1
	while Nspoke < jring1:
		Nspoke *= 2
	if Dmin <= 1:
		jring0 = 1
		jspoke0, jspoke1 = 0, 6 * Nspoke
	else:
		jring0 = max(1, int(Dmin / Dring))
		Acenter = math.atan2(y0, x0)
		dA = min(1.5 * mradius / Dmin, math.tau / 2)
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
	perform.stop("minimapgrid")

	def drawcircleG(posG, rV, color, ocolor=None):
		pM = MconvertG(posG)
		if color is not None:
			pygame.draw.circle(img, color, pM, T(k * rV))
		if ocolor is not None:
			pygame.draw.circle(img, ocolor, pM, T(k * rV), k)

	perform.stop("minimapsetup")
	perform.start("drawminimapspots")
	for spot in state.spots:
		if spot.unlocked and view.beyondminimap(spot) < 5 + settings.countradius:
			rV = 4 * spot.r ** 0.5 * s / mradius
			drawcircleG(spot.pos, rV, (0, 50, 50), (0, 200, 200))
			if state.techlevel["count"] > 0:
				ptext.draw(f"{spot.nunfound()}", center = MconvertG(spot.pos), fontsize = T(3 * rV), owidth = 0.5,
					color = "#7f7fff", surf=img)
			rV = settings.countradius * s / mradius
			pygame.draw.circle(img, (30 * k, 15 * k, 0), MconvertG(spot.pos), T(k * rV), 1)
	perform.stop("drawminimapspots")
	perform.start("drawminimapDM")
	for DM in state.DMtracker.active:
		if DM.found:
			drawcircleG(DM.pos, 3, (0, 0, 0), (0, 200, 200))
		elif not DM.isunfound():
			rV = DM.r * s / mradius
			drawcircleG(DM.pos, rV, (40, 40, 40), (60, 60, 60))
	perform.stop("drawminimapDM")
	drawcircleG(state.you.pos, 4, (80, 0, 0), (160, 0, 0))
	if k != 1:
		img = pygame.transform.smoothscale(img, (2 * s, 2 * s))
	rect = img.get_rect(bottomright = T(1270, 710))
	pview.screen.blit(img, rect)
	pygame.draw.rect(pview.screen, (60, 120, 120), rect, 1)
	perform.stop("drawminimap")





