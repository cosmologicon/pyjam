from __future__ import division
import pygame, math
from src import window, ptext, state, image
from src.window import F

lines = []

def clear():
	del lines[:]

def show(line, t0 = None):
	lines.append([line, t0, 0])
def hide(line):
	lines[:] = [[l, t0, t] for l, t0, t in lines if l != line]

def think(dt):
	nlines = []
	for line, t0, t in lines:
		t += dt
		if t0 is None or t < t0:
			nlines.append([line, t0, t])
	lines[:] = nlines

def draw():
	for line, t0, t in lines:
		alpha = min(2 * t, 1, (2 * (t0 - t) if t0 is not None else 1))
		ptext.draw(line, fontsize = F(32), midtop = F(854 / 2, 10), color = "gray",
			owidth = 1, alpha = alpha, fontname = "Orbitron")

def dump():
	return lines
def load(obj):
	lines[:] = obj

minimap = None
def drawminimap():
	global minimap
	w = F(120)
	scale = window.f
	if minimap is None or minimap.get_size() != (w, w):
		minimap = pygame.Surface((w, w)).convert_alpha()
	minimap.fill((255, 255, 255, 30))
	p0 = window.windowpos(0, 0, w, w, window.camera.X0, window.camera.y0, scale)
	for r in range(25, state.R + 25, 25):
		pygame.draw.circle(minimap, (255, 255, 255, 60), p0, int(scale * r), F(1))
	for j in range(48):
		r0 = 25 * (8 if j % 2 else 4 if j % 4 else 2 if j % 8 else 1)
		X = math.tau * j / 48
		p1 = window.windowpos(X, r0, w, w, window.camera.X0, window.camera.y0, scale)
		p2 = window.windowpos(X, state.R, w, w, window.camera.X0, window.camera.y0, scale)
		pygame.draw.line(minimap, (255, 255, 255, 60), p1, p2, F(1))
	objs = [(state.you, (200, 200, 200))]
	objs += [(g, (200, 0, 200)) for g in state.goals]
	for obj, color in objs:
		p = window.windowpos(obj.X, obj.y, w, w, window.camera.X0, window.camera.y0, scale)
		pygame.draw.circle(minimap, color, p, F(2))
	pygame.draw.rect(minimap, (255, 255, 255, 60), (0, 0, w, w), F(3))
	window.screen.blit(minimap, minimap.get_rect(right = window.sx - F(10), top = F(10)))

fullmap = None
def drawmap():
	global fullmap
	w = F(420)
	scale = 200 / state.R
	if fullmap is None or fullmap.get_size() != (w, w):
		fullmap = pygame.Surface((w, w)).convert_alpha()
	fullmap.fill((0, 0, 0, 120))
	p0 = w // 2, w // 2
	for r in range(25, state.R + 25, 25):
		pygame.draw.circle(fullmap, (255, 255, 255, 60), p0, int(scale * r), F(1))
	for j in range(48):
		r0 = 25 * (8 if j % 2 else 4 if j % 4 else 2 if j % 8 else 1)
		X = math.tau * j / 48
		p1 = window.windowpos(X, r0, w, w, 0, 0, scale)
		p2 = window.windowpos(X, state.R, w, w, 0, 0, scale)
		pygame.draw.line(fullmap, (30, 60, 30), p1, p2, F(1))
	objs = []
	if 0.001 * pygame.time.get_ticks() % 0.5 < 0.25:
		objs += [(state.you, (200, 200, 200))]
	objs += [(g, (200, 0, 200)) for g in state.goals]
	for obj, color in objs:
		p = window.windowpos(obj.X, obj.y, w, w, 0, 0, scale)
		pygame.draw.circle(fullmap, color, p, F(2))
	pygame.draw.rect(fullmap, (255, 255, 255, 120), (0, 0, w, w), F(3))
	window.screen.blit(fullmap, fullmap.get_rect(center = window.screen.get_rect().center))

shipdata = {
	"Skiff": ("Skiff", "fast", None),
	"Mapper": ("Survey", "slow", "view map"),
	"Beacon": ("Detector", "slow", "find hidden"),
	"WarpShip": ("Warp Ship", "medium", "warp"),
}


statsbox = None
def drawstats():
	global statsbox
	if not state.you:
		return
	w = F(80)
	if statsbox is None or statsbox.get_size() != (w, w):
		statsbox = pygame.Surface((w, w)).convert_alpha()
	statsbox.fill((0, 0, 0, 30))
	img = image.get(state.you.imgname, s = F(60))
	statsbox.blit(img, img.get_rect(center = statsbox.get_rect().center))
	pygame.draw.rect(statsbox, (255, 255, 255, 40), (0, 0, w, w), F(3))
	window.screen.blit(statsbox, statsbox.get_rect(left = F(10), top = F(10)))
	shipname, handling, special = shipdata[state.you.__class__.__name__]
	text = "\n".join([
		"Current ship: %s" % shipname,
		"Handling: %s" % handling,
		"Tap space: %s" % special if special is not None else "",
	])
	ptext.draw(text, topleft = F(104, 40), fontsize = F(16), shadow = (1, 1),
		lineheight = 1.3, alpha = 0.5, fontname = "Exo")
	x0, y0, w, h, dx, thick = F(104, 10, 16, 20, 20, 2)
	for j in range(state.you.maxhp):
		pygame.draw.rect(window.screen, (0, 100, 0),
			(x0 + j * dx, y0, w, h), (0 if j < state.you.hp else thick))



