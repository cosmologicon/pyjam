import pygame, math
from src import window, ptext, state
from src.window import F

lines = []

def clear():
	del lines[:]

def show(line):
	lines.append(line)

def think(dt):
	clear()

def draw():
	for line in lines:
		ptext.draw(line, fontsize = F(40), midtop = F(window.sx / 2, 10), color = "gray",
			owidth = 1)

minimap = None
def drawminimap():
	global minimap
	w = F(120)
	scale = window.f
	if minimap is None or minimap.get_size() != (w, w):
		minimap = pygame.Surface((w, w)).convert_alpha()
	minimap.fill((255, 255, 255, 30))
	p0 = window.windowpos(0, 0, w, w, window.cameraX0, window.cameray0, scale)
	for r in range(25, state.R + 25, 25):
		pygame.draw.circle(minimap, (255, 255, 255, 60), p0, int(scale * r), F(1))
	for j in range(48):
		r0 = 25 * (8 if j % 2 else 4 if j % 4 else 2 if j % 8 else 1)
		X = math.tau * j / 48
		p1 = window.windowpos(X, r0, w, w, window.cameraX0, window.cameray0, scale)
		p2 = window.windowpos(X, state.R, w, w, window.cameraX0, window.cameray0, scale)
		pygame.draw.line(minimap, (255, 255, 255, 60), p1, p2, F(1))
	objs = [(state.you, (200, 200, 200))]
	objs += [(g, (200, 0, 200)) for g in state.goals]
	for obj, color in objs:
		p = window.windowpos(obj.X, obj.y, w, w, window.cameraX0, window.cameray0, scale)
		pygame.draw.circle(minimap, color, p, F(2))
	pygame.draw.rect(minimap, (255, 255, 255, 60), (0, 0, w, w), F(3))
	window.screen.blit(minimap, minimap.get_rect(right = window.sx - F(10), top = F(10)))

