from __future__ import division
import pygame, math, sys, os.path, json, random
from pygame.locals import *
sys.path.insert(1, sys.path[0] + "/..")
from src import ptext

tau = 2 * math.pi

R = 500
Rcore = 30
payloads = []
filaments = []
convergences = []

for j in range(6):
	X0 = (j / 6 + 0.5) * tau
	y0 = [100, 240, 180, 300, 130, 250][j]
	convergences.extend([
		(X0, y0),
		(X0 + 0.15, y0 + 100),
		(X0 - 0.2, y0 + 130),
	])

convergences = [
	(random.uniform(0, tau), random.uniform(Rcore + 30, R - 30))
	for _ in range(20)
]
convergences = [
	(tau / 1.618 * j, 100 * math.sqrt(j)) for j in range(1, 21)
]

if os.path.exists("data/worlddata.json"):
	data = json.load(open("data/worlddata.json", "r"))
	for varname, var in data.items():
		globals()[varname] = var

sx = sy = 800
scale = 0.45 * min(sx, sy) / R
def screenpos(X, y):
	return int(round(sx / 2 + scale * y * math.sin(X))), int(round(sy / 2 - scale * y * math.cos(X)))
def worldpos(px, py):
	ax = (px - sx / 2) / scale
	ay = (-py + sy / 2) / scale
	return math.atan2(ax, ay), math.sqrt(ax ** 2 + ay ** 2)
screen = pygame.display.set_mode((sx, sy))

playing = True
while playing:
	mX, my = worldpos(*pygame.mouse.get_pos())

	kpressed = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			playing = False
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN and event.key == K_p:
			if kpressed[K_BACKSPACE]:
				if payloads:
					payloads.pop()
			else:
				payloads.append((mX, my))
		if event.type == KEYDOWN and event.key == K_g:
			if kpressed[K_BACKSPACE]:
				if filaments:
					filaments.pop()
			else:
				filaments.append([])
		if event.type == KEYDOWN and event.key == K_f:
			if kpressed[K_BACKSPACE]:
				if filaments[-1]:
					filaments[-1].pop()
			else:
				filaments[-1].append((mX, my))
	
	screen.fill((0,0,0))
	pygame.draw.circle(screen, (0, 30, 0), screenpos(0, 0), int(R * scale), 0)
	pygame.draw.circle(screen, (0, 60, 0), screenpos(0, 0), int(R * scale), 2)
	for j in range(6):
		X0 = j * tau / 12
		X1 = X0 + tau / 2
		pygame.draw.line(screen, (0, 60, 0), screenpos(X0, R), screenpos(X1, R), 1)
	pygame.draw.circle(screen, (0, 100, 0), screenpos(0, 0), int(Rcore * scale), 0)
	pygame.draw.circle(screen, (0, 60, 0), screenpos(0, 0), int(160 * scale), 1)
	pygame.draw.circle(screen, (0, 60, 0), screenpos(0, 0), int(260 * scale), 1)
	pygame.draw.circle(screen, (0, 60, 0), screenpos(0, 0), int(340 * scale), 1)
	for X, y in payloads:
		pygame.draw.circle(screen, (255, 0, 255), screenpos(X, y), 2)
	for X, y in convergences:
		pygame.draw.circle(screen, (255, 255, 255), screenpos(X, y), 2)
	for filament in filaments:
		if len(filament) > 1:
			pygame.draw.lines(screen, (255, 255, 0), False, [screenpos(X, y) for X, y in filament])
	ptext.draw("%.3f, %.0f" % (mX, my), bottomleft = (5, sy - 5))
	pygame.display.flip()

obj = {
	"R": R,
	"Rcore": Rcore,
	"payloads": payloads,
	"filaments": filaments,
	"convergences": convergences,
}
json.dump(obj, open("data/worlddata.json", "w"))

