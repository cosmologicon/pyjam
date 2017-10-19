from __future__ import division, print_function
import pygame, math
from . import pview

def i(x):
	return max(int(round(x)), 1)

def drawfoot(pos, scale):
	x, y = pos
	pos = i(x), i(y)
	pygame.draw.circle(pview.screen, (0, 0, 0), pos, i(1 * scale))
	pygame.draw.circle(pview.screen, (200, 200, 150), pos, i(0.7 * scale))

def drawnoggin(pos, scale):
	x, y = pos
	pos = i(x), i(y)
	pos2 = i(x - 0.8 * scale), i(y - 0.6 * scale)
	color = 200, 200, 150
	pygame.draw.circle(pview.screen, (0, 0, 0), pos, i(1.4 * scale))
	pygame.draw.circle(pview.screen, (0, 0, 0), pos2, i(1.1 * scale))
	pygame.draw.circle(pview.screen, color, pos, i(1.1 * scale))
	pygame.draw.circle(pview.screen, color, pos2, i(0.8 * scale))
	
	

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
	pygame.draw.circle(pview.screen, (255, 0, 255), screenpos, i(0.3 * scale))
	# torso
	x0, y0 = x - 0.3 * scale, y - (1.7 + 0.2 * S2) * scale
	path = [(-2.5, 0), (-1, -0.5), (1.5, -0.8), (2, 3), (1, 3.2)]
	ps = [(i(x0 + scale * dx), i(y0 - scale * dy)) for dx, dy in path]
	pygame.draw.polygon(pview.screen, (0, 0, 0), ps, i(0.6 * scale))
	pygame.draw.polygon(pview.screen, (100, 100, 250), ps, 0)
	# front fist
	x0 += 0.5 * scale
	y0 -= 1.2 * scale
	dx, dy = 1.6 * fC, 0.4 * abs(S)
	drawfoot((x0 + dx * scale, y0 + dy * scale), scale)
	# noggin
	Snoggin = math.sin(2 * fcycle * math.tau - 0.6)
	x0, y0 = x + 1.1 * scale, y - (5 + 0.2 * Snoggin) * scale
	drawnoggin((x0, y0), scale)
		

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
		pygame.display.flip()

