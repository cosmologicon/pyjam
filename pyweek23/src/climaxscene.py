import math, random, pygame
from pygame.locals import *
from . import view, state, thing, background, settings, hud, util
from .util import F

def init():
	state.reset()
	state.you = thing.You(x = -200, y = 0)
	state.yous.append(state.you)
	state.yous.append(thing.Him())
	state.scrollspeed = 0


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
		dx, dy = state.you.x - 300, state.you.y
		d = math.sqrt(dx ** 2 + dy ** 2)
		dx, dy = util.norm(dx, dy, state.speed * 0.5 / (1 + (d / 1000) ** 2))
		state.you.x += dx * dt
		state.you.y += dy * dt
	view.think(dt)
	for x in state.yous:
		x.think(dt)


def draw():
	background.draw()
	for _ in range(5):
		rect = F(pygame.Rect((0, 0, random.randrange(8, 200), random.randrange(8, 200))))
		rect.center = view.screenpos((300, 0))
		color = [random.randint(120, 255) for _ in range(3)]
		pygame.draw.ellipse(view.screen, color, rect, F(3))
	for x in state.yous:
		x.draw()
	dx, dy = state.you.x - 300, state.you.y
	d = math.sqrt(dx ** 2 + dy ** 2)
	a = util.clamp(220 - 1 * d, 0, 220)
	copy = view.screen.convert_alpha()
	copy.fill((255, 255, 255, a))
	view.screen.blit(copy, (0, 0))

