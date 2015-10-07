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
		ptext.draw(line, fontsize = F(24), midtop = F(854 / 2, 80), width = F(460), color = "gray",
			owidth = 1, alpha = alpha, fontname = "Orbitron", lineheight = 1.2)

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
	global fullmap, grid
	w = F(420)
	scale = F(200) / state.R
	if fullmap is None or fullmap.get_size() != (w, w):
		fullmap = pygame.Surface((w, w)).convert_alpha()
		grid = pygame.Surface((w, w)).convert()
		grid.fill((0, 0, 0))
		p0 = w // 2, w // 2
		for filament in state.worlddata["filaments"]:
			ps = [window.windowpos(X, y, w, w, 0, 0, scale) for X, y in filament]
			pygame.draw.lines(grid, (40, 40, 0), False, ps, F(6))
		for r in range(25, state.R + 25, 25):
			pygame.draw.circle(grid, (10, 40, 10), p0, int(scale * r), F(1))
		pygame.draw.circle(grid, (200, 0, 0), p0, int(scale * state.R), F(1))
		pygame.draw.circle(grid, (200, 0, 0), p0, int(scale * state.Rcore), F(1))
		for j in range(48):
			r0 = 25 * (8 if j % 2 else 4 if j % 4 else 2 if j % 8 else 1)
			X = math.tau * j / 48
			p1 = window.windowpos(X, r0, w, w, 0, 0, scale)
			p2 = window.windowpos(X, state.R, w, w, 0, 0, scale)
			pygame.draw.line(grid, (10, 40, 10), p1, p2, F(1))
		ptext.draw("The Charybdis\nAnomaly", fontname = "Exo", fontsize = F(19),
			bottomleft = F(10, 410), owidth = 2, surf = grid)
		ptext.draw("OUTER HORIZON", fontname = "Exo", fontsize = F(14),
			center = F(70, 70), angle = 45, color = (200, 0, 0), owidth = 2, surf = grid)
		ptext.draw("OUTER HORIZON", fontname = "Exo", fontsize = F(14),
			center = F(420-70, 70), angle = -45, color = (200, 0, 0), owidth = 2, surf = grid)
		ptext.draw("OUTER HORIZON", fontname = "Exo", fontsize = F(14),
			center = F(420-70, 420-70), angle = 45, color = (200, 0, 0), owidth = 2, surf = grid)
		ptext.draw("DATA\nHORIZON", fontname = "Exo", fontsize = F(14),
			center = F(210, 210), color = (200, 0, 0), owidth = 2, surf = grid)
		ptext.draw("DANGER", fontname = "Exo", fontsize = F(14),
			center = F(160, 126), angle = -5, color = (100, 100, 0), owidth = 2, surf = grid)
		ptext.draw("DANGER", fontname = "Exo", fontsize = F(14),
			center = F(270, 244), angle = 6, color = (100, 100, 0), owidth = 2, surf = grid)
		ptext.draw("DANGER", fontname = "Exo", fontsize = F(14),
			center = F(295, 70), angle = -70, color = (100, 100, 0), owidth = 2, surf = grid)
		grid.set_alpha(180)
	window.screen.blit(grid, grid.get_rect(center = window.screen.get_rect().center))

	fullmap.fill((0, 0, 0, 0))
	objs = []
	if 0.001 * pygame.time.get_ticks() % 0.5 < 0.25:
		objs += [(state.you, (200, 200, 200), False)]
	objs += [(g, (200, 0, 200), g.isvisible()) for g in state.goals]
	for obj, color, outline in objs:
		p = window.windowpos(obj.X, obj.y, w, w, 0, 0, scale)
		pygame.draw.circle(fullmap, color, p, F(2))
		if outline:
			pygame.draw.circle(fullmap, color, p, F(5), F(1))
			pygame.draw.circle(fullmap, color, p, F(8), F(1))
		name = "YOU" if obj is state.you else {
			"Payload": "DATA CORE",
			"BatesShip": "DISTRESS\nCALL",
			"Convergence": "???",
		}[obj.__class__.__name__]
		ptext.draw(name, fontname = "Exo", fontsize = F(12), owidth = 2, surf = fullmap,
			color = color, centerx = p[0], top = p[1] + F(1))
	pygame.draw.rect(fullmap, (255, 255, 255, 120), (0, 0, w, w), F(3))
	window.screen.blit(fullmap, fullmap.get_rect(center = window.screen.get_rect().center))

shipdata = {
	"Skiff": ("Cutter", None),
	"Heavy": ("Armored", None),
	"HeavySkiff": ("Armored Cutter", None),

	"Mapper": ("Survey Ship", "toggle map"),
	"HeavyMapper": ("Armored Survey", "toggle map"),
	"HeavyMapperSkiff": ("Armored Survey Cutter", "toggle map"),

	"Beacon": ("Detector", "find hidden"),
	"BeaconSkiff": ("Cutter-Detector", "find hidden"),
	"HeavyBeacon": ("Armored Detector", "find hidden"),
	"HeavyBeaconSkiff": ("Armored Cutter-Detector", "find hidden"),

	"Warp": ("Warp Ship", "warp"),
	"WarpSkiff": ("Warp Cutter", "warp"),
	"HeavyWarpSkiff": ("Armored Warp Cutter", "warp"),
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
	shipname, special = shipdata[state.you.__class__.__name__]
	text = "\n".join([
		"Current ship: %s" % shipname,
		"Hold space: teleport",
		"Tap space: %s" % special if special is not None else "",
		"Backspace: emergency teleport",
	])
	ptext.draw(text, topleft = F(10, 104), fontsize = F(16), shadow = (1, 1),
		lineheight = 1.1, alpha = 0.5, fontname = "Exo")
	x0, y0, w, h, dx, thick = F(104, 10, 16, 20, 20, 2)
	for j in range(state.you.maxhp):
		pygame.draw.rect(window.screen, (0, 100, 0),
			(x0 + j * dx, y0, w, h), (0 if j < state.you.hp else thick))



