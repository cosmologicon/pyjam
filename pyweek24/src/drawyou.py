from __future__ import division, print_function
import pygame, math, settings
from . import pview

scolor = 200, 100, 250

def i(x):
	return max(int(round(x)), 1)

def drawfoot(pos, scale):
	x, y = pos
	pos = i(x), i(y)
	pygame.draw.circle(pview.screen, (0, 0, 0), pos, i(1 * scale))
	pygame.draw.circle(pview.screen, scolor, pos, i(0.7 * scale))

def drawnoggin(pos, scale, angle = 0):
	x, y = pos
	C, S = math.CS(angle)
	def p(dx, dy):
		dx, dy = C * dx + S * dy, -S * dx + C * dy
		return (i(x + dx * scale), i(y + dy * scale))
	pygame.draw.circle(pview.screen, (0, 0, 0), p(0, 0), i(1.4 * scale))
	pygame.draw.circle(pview.screen, scolor, p(0, 0), i(1.1 * scale))
	ps = [p(dx, dy) for dx, dy in [(-1.5, 0), (2, -1.5), (-4, -1), (-1.8, -2.5)]]
	pygame.draw.polygon(pview.screen, (240, 40, 180), ps)
	pygame.draw.lines(pview.screen, (0, 0, 0), True, ps, i(0.3 * scale))
	pygame.draw.line(pview.screen, (0, 0, 0), p(0.2, 0.3), p(0.3, -0.7), i(0.3 * scale))
	pygame.draw.line(pview.screen, (255, 255, 255), p(0.45, 0.1), p(0.5, -0.5), i(0.3 * scale))
	

def running(screenpos, scale, fcycle):
	x, y = screenpos
	C, S = math.CS(fcycle * math.tau)
	C2, S2 = math.CS(2 * fcycle * math.tau)
	# foots
	x0, y0 = x - 1 * scale, y - 1 * scale
	fC = abs(C) ** 0.7 * math.sign(C)
	dx = 1.3 * fC
	dy = 0.4 * S + 0.2 * C
	drawfoot((x0 + dx * scale, y0 + dy * scale), scale)
	drawfoot((x0 - dx * scale, y0 - dy * scale), scale)
	# back fist
	x0 = x + 0.2 * scale
	y0 = y + (-2.9 - 0.2 * S2) * scale
	dx, dy = 1.6 * fC, 0.4 * abs(S)
	drawfoot((x0 - dx * scale, y0 + dy * scale), scale)
	# dress
	x0, y0 = x - 0.3 * scale, y - (1.7 + 0.2 * S2) * scale
	path = [(-2.5, 0), (-0.5, -0.5), (1.5, -0.8), (1.5, 1), (2, 3), (1, 3.2), (-0.7, 1.5)]
	ps = [(i(x0 + scale * dx), i(y0 - scale * dy)) for dx, dy in path]
	pygame.draw.polygon(pview.screen, (0, 0, 0), ps, i(0.6 * scale))
	pygame.draw.polygon(pview.screen, (100, 100, 250), ps, 0)
	# front fist
	x0 = x + 0.2 * scale
	y0 = y + (-2.9 - 0.2 * S2) * scale
	dx, dy = 1.6 * fC, 0.4 * abs(S)
	drawfoot((x0 + dx * scale, y0 + dy * scale), scale)
	# noggin
	Snoggin = math.sin(2 * fcycle * math.tau - 0.6)
	x0, y0 = x + 1.1 * scale, y - (5 + 0.2 * Snoggin) * scale
	drawnoggin((x0, y0), scale, angle = 0.2 + 0.1 * Snoggin)

	if settings.DEBUG:
		pygame.draw.circle(pview.screen, (255, 0, 255), screenpos, i(0.3 * scale))

def falling(screenpos, scale, vy):
	vy = math.clamp(vy, -30, 30)
	x, y = screenpos
	dystretch = vy / 70
	drawfoot((x - 0.8 * scale, y + (-0.2 + dystretch) * scale), scale)
	drawfoot((x + 0.8 * scale, y + (0.2 + dystretch) * scale), scale)

	# back fist
	drawfoot((x + (1.5 * math.cos(dystretch)) * scale, y + (-2.5 + 3 * dystretch) * scale), scale)

	# dress
	x0, y0 = x - 0.3 * scale, y - 1 * scale
	path = [(-1.4, 0), (-0.2, -0.5), (2, -0.5), (1.5, 1), (1, 3), (0, 3.2), (-1, 1.5)]
	ps = [(i(x0 + scale * dx * (1 - 0.6 * dystretch)), i(y0 - scale * (dy / (1 - 0.3 * dystretch) - 1.3 * dystretch))) for dx, dy in path]
	pygame.draw.polygon(pview.screen, (0, 0, 0), ps, i(0.6 * scale))
	pygame.draw.polygon(pview.screen, (100, 100, 250), ps, 0)

	# front fist
	drawfoot((x - (1.5 * math.cos(dystretch)) * scale, y + (-2.5 + 3 * dystretch) * scale), scale)

	# noggin
	x0, y0 = x + 0.5 * scale, y - 5 * scale
	drawnoggin((x0, y0), scale, angle = 0.2 + 0.5 * dystretch)


	if settings.DEBUG:
		pygame.draw.circle(pview.screen, (255, 0, 255), screenpos, i(0.3 * scale))

def dying(screenpos, scale):
	falling(screenpos, scale, 0)
	

if __name__ == "__main__":
	from . import maff, view
	view.init()
	clock = pygame.time.Clock()
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		clock.tick()
		pview.fill((0, 0, 200))
		fcycle = pygame.time.get_ticks() / 5000 % 1
		running((512, 400), 40, fcycle)
		fcycle = pygame.time.get_ticks() / 500 % 1
		running((212, 400), 40, fcycle)
		running((100, 200), 8, fcycle)

		fcycle = pygame.time.get_ticks() / 3000 % 1
		vy = 30 * math.cos(fcycle * math.tau / 2)
		falling((800, 200), 16, vy)

		pygame.display.flip()

