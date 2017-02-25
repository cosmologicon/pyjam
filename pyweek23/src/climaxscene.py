import math, random, pygame
from pygame.locals import *
from . import view, state, thing, background, settings, hud, util, sound, scene, winscene
from .util import F

def init():
	global spawner, twin, popped
	state.clear()
	state.restart()
	state.stage = "climax"
	state.good = True
	state.you = thing.You(x = -200, y = 50)
	state.yous.append(state.you)
	state.yous.append(thing.Him())
	spawner = sound.Dplayer("climax")
	state.scrollspeed = 0
	twin = 0
	popped = False
	state.saved.add("J")
	state.met.add("J")
	state.met.add("C")
	state.met.add("7")
	sound.mplay(2)


def think(dt, kdowns, kpressed):
	global twin, popped
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
		dx, dy = state.you.x - 300, state.you.y
		d = math.sqrt(dx ** 2 + dy ** 2)
		dx, dy = util.norm(dx, dy, state.speed * 0.5 / (1 + (d / 1000) ** 2))
		state.you.x += dx * dt
		state.you.y += dy * dt
	view.think(dt)
	if spawner.alive:
		spawner.think(dt)

	if state.you.alive and not spawner.alive:
		twin += dt
		state.you.x += twin * 1000 * dt
		if state.you.x > 1000:
			if not popped:
				poppped = True
				state.best = False
				scene.pop()
				scene.push(winscene)
	else:
		for x in state.yous:
			x.think(dt)


	if state.you.alive:
		dx, dy = state.you.x - 300, state.you.y
		d = math.sqrt(dx ** 2 + dy ** 2)
		if d < 20:
			spawner.alive = False
			sound.dplay("C10")
			state.you.alive = False
			state.you.x = 300
			state.you.y = 0
	else:
		twin += dt
		if twin > 2 and not popped:
			poppped = True
			state.best = True
			state.saved.add("C")
			scene.pop()
			scene.push(winscene)


def draw():
	background.draw()
	for _ in range(5):
		rect = F(pygame.Rect((0, 0, random.randrange(8, 200), random.randrange(8, 200))))
		rect.center = view.screenpos((300, 0))
		color = [random.randint(120, 255) for _ in range(3)]
		pygame.draw.ellipse(view.screen, color, rect, F(3))
	for x in state.yous:
		x.draw()
	a = util.clamp(255 * (22 - state.you.t), 0, 255)
	if a:
		copy = view.screen.convert_alpha()
		copy.fill((0, 0, 0, a))
		view.screen.blit(copy, (0, 0))
	

	spawner.draw()
	dx, dy = state.you.x - 300, state.you.y
	d = math.sqrt(dx ** 2 + dy ** 2)
	a = util.clamp(255 - 1 * d, 0, 255)
	copy = view.screen.convert_alpha()
	copy.fill((255, 255, 255, a))
	view.screen.blit(copy, (0, 0))

