from __future__ import division
import math
from pygame.locals import *
from . import view, state, thing, background, settings, hud, util, randomdata, sound

def init(stage):
	global tlastsave
	state.clear()
	state.restart()
	state.stage = stage
	state.you = thing.You(x = -300, y = 0)
	state.yous.append(state.you)
	makewaves()
	tlastsave = 0

def think(dt, kdowns, kpressed):
	global tlastsave
	sound.mplay(2)
	if settings.isdown("swap", kdowns):
		settings.swapaction = not settings.swapaction
	if state.you.alive:
		dx = settings.ispressed("right", kpressed) - settings.ispressed("left", kpressed)
		dy = settings.ispressed("down", kpressed) - settings.ispressed("up", kpressed)
		if settings.portrait:
			dx, dy = -dy, dx
		if dx and dy:
			dx *= math.sqrt(0.5)
			dy *= math.sqrt(0.5)
		state.you.move(dt, dx, dy)
		if settings.ispressed("action", kpressed) != settings.swapaction:
			state.you.act()
	view.think(dt)
	state.think(dt)
	if settings.tquicksave and state.you.alive and not state.twin and not state.tlose:
		dt = state.you.t - tlastsave
		if dt >= settings.tquicksave:
			tlastsave = state.you.t
			state.save(settings.quicksavefile)

def draw():
	if settings.lowres:
		view.screen.fill((0, 0, 0))
	else:
		background.draw(stage = state.stage)
#	background.drawrift()
	state.draw()
	hud.draw()
	if state.tlose:
		alpha = util.clamp(state.tlose - 2, 0, 1)
		surf = view.screen.convert_alpha()
		surf.fill((0, 0, 0, int(alpha * 255)))
		view.screen.blit(surf, (0, 0))
	if state.twin > 2:
		alpha = util.clamp(state.twin - 2, 0, 1)
		surf = view.screen.convert_alpha()
		surf.fill((200, 200, 255, int(alpha * 255)))
		view.screen.blit(surf, (0, 0))

def makewaves():
	if state.stage == 1:
		state.waves = [
			[0, adddplayer, "intro"],
			[0, state.addduckwave, 700, 500, 4, 4, [
				[0, 350, 100],
				[4, 200, -200],
				[8, 0, 100],
				[12, -600, 200],
			]],
			[0, state.addduckwave, 700, -500, 4, 4, [
				[0, 350, -100],
				[4, 200, 200],
				[8, 0, -100],
				[12, -600, -200],
			]],
			[0, addheronsplash, 2, 2],
			[20, addemu],
		]
	if state.stage == 2:
		state.waves = [
			[0, addcapsule, 1, 0, 0, -20, 0],
			[40, addcapsule, 2, 500, 100, -40, 0],
			[80, addcapsule, 3, 500, 0, -40, 6],

			[0, addheronsplash, 1, 4, 600],
			[10, addheronsplash, 1, 4, 600],
			#[60, addheronsplash, 1, 6, 600],
			[30, state.addturkeywave, 700, 0, 1, 8, [
				[0, 250, 0],
				[8, -700, 0],
			]],
			[30, state.addturkeywave, 700, 0, 1, 8, [
				[0, 350, 0],
				[12, -700, 0],
			]],
			[30, state.addturkeywave, 700, 0, 1, 8, [
				[0, 450, 0],
				[16, -700, 0],
			]],
			[30, addlarkwave, 10, 200, 0, -100, 500, 200],
			[40, addlarkwave, 10, -100, 0, 100, -500, 200],

			[30, addasteroids, 60, 1400],

			[60, addclusterbombs, 20, 40, 0, 400, 600, 0, -60, -60],
			[64, addclusterbombs, 20, 40, 0, -400, 600, 0, -60, 60],

			[96, addlarkwave, 10, 200, 120, -100, 300, 200],
			[102, addlarkwave, 10, 200, -120, 100, -300, 200],
			[100, addlarkwave, 10, -100, 120, -100, 300, 200],
			[98, addlarkwave, 10, -100, -120, 100, -300, 200],

			[100, state.addegret],

		]
	if state.stage == 3:
		state.waves = [
			[0, addcapsule, 4, 520, 260, -40, 0],
			[45, addcapsule, 5, 330, -400, -5, 40],
			[90, addcapsule, 6, 500, 0, -100, -40],

			[5, state.addduckwave, 700, 500, 4, 4, [
				[0, 350, 100],
				[4, 200, -200],
				[8, 0, 100],
				[12, -600, 200],
			]],
			[5, state.addduckwave, 700, -500, 4, 4, [
				[0, 350, -100],
				[4, 200, 200],
				[8, 0, -100],
				[12, -600, -200],
			]],

			[0, addheronsplash, 2, 4, 1000],
			[0, addcobra, 20, 40, 500, 300, -450, -100, 0, 100],
			[5, addcobra, 20, 40, 500, -300, -450, 100, 0, 100],
			[15, addasteroids, 50, 1200, 123],
			[15, addbluerock, 1200, 220, -40, 0],
			[35, addcobra, 40, 80, 500, 0, -1400, 0, 0, 320],
			[35, addcobra, 40, 80, 1000, 0, -1400, 0, -500, 320],

			[55, addclusterbombs, 20, 40, 0, 400, 600, 0, -60, -60],
			[59, addclusterbombs, 20, 40, 0, -400, 600, 0, -60, 60],

			[80, addcobra, 20, 40, -400, 500, 0, -500, 0, 100],
			[83, addcobra, 20, 40, -250, -500, 0, 500, 0, 100],
			[86, addcobra, 20, 40, -100, 500, 0, -500, 0, 100],
			[89, addcobra, 20, 40, 50, -500, 0, 500, 0, 100],
			[92, addcobra, 20, 40, 200, 500, 0, -500, 0, 100],
			[95, addcobra, 20, 40, 350, -500, 0, 500, 0, 100],
			[90, addlarkwave, 10, 200, 0, -100, 500, 200],
			[90, addlarkwave, 10, -100, 0, 100, -500, 200],

			[105, state.addmedusa],
		]
	if state.stage == 4:
		state.waves = [
			[0, addgabriel],
			[6, adddplayer, "A"],
			[6, addhawk],
		]

def addcapsule(name, x, y, vx, vy):
	if str(name) in state.saved:
		return
	state.planets.append(thing.Capsule(name = name, x = x, y = y, vx = vx, vy = vy))
	
def addemu():
	state.bosses.append(thing.Emu(x = 600, y = 0, xtarget = 100))

def addhawk():
	state.bosses.append(thing.Hawk(x = 600, y = 0, xtarget = 200))

def addheronsplash(nx, ny, x0 = 1000):
	for ax in range(nx):
		for ay in range(ny):
			state.enemies.append(thing.Heron(
				x = x0,
				y = (ay - (ny - 1) / 2) / ny * 2 * 300,
				vx = -40 - 20 * ax,
				vy = 0
			))
			
def addlarkwave(n, x0, y0, vy0, dy0, cr):
	dj = 20 if vy0 < 0 else -20
	for j in range(n):
		state.enemies.append(thing.Lark(x0 = x0, y0 = y0, dy0 = dy0 + dj * j, vy0 = vy0, cr = cr, dydtheta = 50))

def addasteroids(n, x0, j0 = 0):
	for j in range(j0, j0 + n):
		dx, dy, dr, dvx = randomdata.rocks[j]
		x = x0 + 200 * dx
		y = (dy * 2 - 1) * state.yrange
		r = round((30 + 40 * dr) / 20) * 20
		vx = -20 - 40 * dvx
		vy = (dvx * 1000 % 1 * 2 - 1) * 2
		rock = thing.Rock(x = x, y = y, vx = vx, vy = vy, r = r, hp = int(r * 0.7))
		state.enemies.append(rock)

def addbluerock(x, y, vx, vy):
	rock = thing.BlueRock(x = x, y = y, vx = vx, vy = vy)
	state.enemies.append(rock)

def addcobra(n, r, x0, y0, dx, dy, p0, h):
	for jseg in range(n):
		state.enemies.append(thing.Cobra(
			x0arc = x0, y0arc = y0, dxarc = dx, dyarc = dy,
			p0arc = p0, harc = h, r = r))
		p0 -= r * 0.8
		r *= 0.95

def addclusterbombs(n, t, x0, y0, dx, dy, vx, vy):
	for j in range(n):
		dt = j / n * t
		x = x0 + j * math.phi % 1 * dx - vx * dt
		y = y0 + j * math.phi % 1 * dy - vy * dt
		state.badbullets.append(thing.BadClusterBullet(x = x, y = y, vx = vx, vy = vy))
		
def addgabriel():
	if state.downgraded:
		state.planets.append(thing.Gabriel(x = 500, y = 500))


def adddplayer(name):
	state.spawners.append(sound.Dplayer(name))




