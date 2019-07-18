from __future__ import division
import pygame, datetime, math, random
from . import settings, state, starmap

scale = settings.grect.width / 2 / settings.vsize
x0, y0 = 0, 0  # center of viewport in world coordinates
X0, Y0 = settings.grect.center  # center of gameplay viewport in screen coordinates
navx0, navy0 = 0, 0
nstars = int(0.002 * settings.grect.width * settings.grect.height)

def clamp(x, a, b):
	return a if x < a else b if x > b else x

def init():
	global screen, stars, navmap
	screen = pygame.display.set_mode(settings.ssize)
	navmap = pygame.Surface(settings.nrect.size).convert()
	stars = sorted([
		(random.uniform(0.05, 1), random.uniform(0, 10000), random.uniform(0, 10000))
		for _ in range(nstars)
	])

def clear():
	screen.fill((0, 0, 0))

def flip():
	pygame.display.flip()

def think(dt):
	global x0, y0, xmin, xmax, ymin, ymax, navx0, navy0
	gw, gh = settings.grect.size
	xmargin, ymargin = gw / 2 / scale, gh / 2 / scale
	x0 = clamp(state.state.you.x, -starmap.rx + xmargin, starmap.rx - xmargin)
	y0 = clamp(state.state.you.y, -starmap.ry + ymargin, starmap.ry - ymargin)
	xmin, xmax = x0 - gw / 2 / scale, x0 + gw / 2 / scale
	ymin, ymax = y0 - gh / 2 / scale, y0 + gh / 2 / scale

	nw, nh = settings.nrect.size
	xmargin, ymargin = nw / 2 / settings.nscale, nh / 2 / settings.nscale
	navx0 = clamp(state.state.you.x, -starmap.rx + xmargin, starmap.rx - xmargin)
	navy0 = clamp(state.state.you.y, -starmap.ry + ymargin, starmap.ry - ymargin)

def worldtoscreen(p):
	x, y = p
	return (
		int(round(X0 + (x - x0) * scale)),
		int(round(Y0 + (y - y0) * scale)),
	)

def worldtonav(p):
	x, y = p
	return (
		int(round(settings.nrect.width / 2 + (x - navx0) * settings.nscale)),
		int(round(settings.nrect.height / 2 + (y - navy0) * settings.nscale)),
	)

def worldtomainmap(p):
	x, y = p
	scale = settings.grect.width / (2 * starmap.rx)
	return (
		int(round(settings.grect.centerx + x * scale)),
		int(round(settings.grect.centery + y * scale)),
	)

def screentoworld(P):
	X, Y = P
	return (
		(X - X0) / scale + x0,
		(Y - Y0) / scale + y0,
	)

def drawnavoort():
	from . import img
	X0, Y0 = worldtonav((0, 0))
	i = img.getimg("oort", scale = settings.nscale / starmap.scale)
	navmap.blit(i, i.get_rect(center = (X0, Y0)))

def drawmainoort():
	from . import img
	scale = settings.grect.width / (2 * starmap.rx)
	img.draw("oort", settings.grect.center, scale = scale)

def drawstars():
	for z, x, y in stars:
		px = int((x - x0) * z * scale) % settings.grect.width
		py = int((y - y0) * z * scale) % settings.grect.height
		c = int(255 * z)
		screen.set_at((px, py), (c, c, c))

def drawbolt(p0, p1, color):
	(x0, y0), (x1, y1) = p0, p1
	dx, dy = x1 - x0, y1 - y0
	if dx ** 2 + dy ** 2 < 1:
		pygame.draw.aaline(screen, color, worldtoscreen((x0, y0)), worldtoscreen((x1, y1)))
		return
	r = random.uniform(-0.3, 0.3)
	xc = (x1 + x0) / 2 + r * dy
	yc = (y1 + y0) / 2 - r * dx
	drawbolt((x0, y0), (xc, yc), color)
	drawbolt((xc, yc), (x1, y1), color)

def isvisible(p, r = 0):
	x, y = p
	return xmin - r < x < xmax + r and ymin - r < y < ymax + r

# Where to put an indicator
def indpos(p):
	x, y = p
	gw, gh = settings.grect.size
	rx, ry = 0.45 * gw / scale, 0.45 * gh / scale
	dx, dy = x - x0, y - y0
	f = rx / abs(dx) if rx * abs(dy) < ry * abs(dx) else ry / abs(dy)
	d = math.sqrt(dx ** 2 + dy ** 2)
	return (x0 + f * dx, y0 + f * dy), math.degrees(math.atan2(-dx, -dy))

def screenshot():
	sname = "screenshot-%s.png" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	pygame.image.save(screen, sname)

