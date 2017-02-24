from __future__ import division
import math
from pygame.locals import *
from . import view, state, thing, background, settings, hud, util

def init(stage):
	state.clear()
	state.restart()
	state.stage = stage
	state.you = thing.You(x = 0, y = 0)
	state.yous.append(state.you)
	makewaves()

def think(dt, kdowns, kpressed):
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


def draw():
	background.draw()
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
			[25, state.addmedusa],
		]
		

	return
	state.waves = [
		[0, state.addduckwave, 700, 0, 4, 6, [
			[0, 350, 0],
			[3, 200, 200],
			[6, 0, -200],
			[9, -600, 0],
		]],
		[5, state.addrockwave, 900, 0, 60, 200],
		[25, state.addmedusa],
	]
#	state.waves = [[0, state.addegret]]
#	state.waves = [[0, state.addmedusa]]
#	state.waves = [[5, state.addrockwave, 900, 0, 60, 200]],
#	state.waves = [[0, state.addheronwave, 10, 1]]
	state.waves = []
#	state.pickups.append(thing.MissilesPickup(x = 300, y = 0))
	state.planets.append(thing.Capsule(x = 100, y = -0, name = 1))
#	state.planets.append(thing.Capsule(x = 1000, y = 300, name = "Falayalaralfali"))
#	state.planets.append(thing.Capsule(x = 1200, y = -200, name = "Unzervalt"))
#	state.enemies.append(thing.Lark(x0 = 0, y0 = 0, dy0 = 400, vy0 = -300, cr = 200, dydtheta = 100))
#	state.enemies.append(thing.Lark(x0 = 0, y0 = 0, dy0 = 300, vy0 = -300, cr = 200, dydtheta = 50))
#	for j in range(10):
#		state.enemies.append(thing.Lark(x0 = 0, y0 = 0, dy0 = 500 + 20 * j, vy0 = -100, cr = 200, dydtheta = 50))
#	state.badbullets.append(thing.BadClusterBullet(x = 400, y = 0, vx = -100, vy = 0))
	
def addemu():
	state.bosses.append(thing.Emu(x = 600, y = 0, xtarget = 100))

def addheronsplash(nx, ny):
	for ax in range(nx):
		for ay in range(ny):
			state.enemies.append(thing.Heron(
				x = 1000,
				y = (ay - (ny - 1) / 2) / ny * 2 * 300,
				vx = -40 - 20 * ax,
				vy = 0
			))
			



