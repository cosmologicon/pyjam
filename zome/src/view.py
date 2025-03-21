from __future__ import division
import pygame, os, os.path, datetime, math
from . import settings, blob, util
from .util import F

screen = None
x0 = 0
y0 = 0
z = 1
Z = math.exp(0.5 * z)

def init():
	global screen, blobscreen, sx, sy
	pygame.display.set_caption(settings.gamename)
	sy = settings.wsize
	flags = 0
	def getsx(sy):
		return (int(round(sy * 16 / 9)) + 1) // 2 * 2
	if settings.fullscreen:
		if sy is None:
			sx0, sy0 = max(pygame.display.list_modes())
			if sx0 * 9 > sy0 * 16:
				sx, sy = getsx(sy0), sy0
			else:
				sx, sy = sx0, int(round(sx0 * 9 / 16))
		else:
			sx = getsx(sy)
		flags = flags or pygame.FULLSCREEN
	else:
		if sy is None:
			sx, sy = 854, 480
		else:
			sx = getsx(sy)
	util.f = sy / 480
	screen = pygame.display.set_mode((sx, sy), flags)

def togglefullscreen():
	settings.fullscreen = not settings.fullscreen
	init()

def screenshot():
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	filename = os.path.join(settings.screenshotpath, "screenshot-%s.png" % timestamp)
	util.mkdir(filename)
	pygame.image.save(screen, filename)

def clear(color = (0, 0, 0)):
	screen.fill(color)

def zoom(dz):
	global z, Z
	z = math.clamp(z + 0.25 * dz, -1, 3)
	Z = math.exp(0.5 * round(z))
	constrain()

# Move the camera such that the given game position is at the given screen coordinate.
def drag(gpos, pos):
	global x0, y0
	x0 = gpos[0] - (pos[0] - sx / 2) / Z / util.f
	y0 = gpos[1] + (pos[1] - sy / 2) / Z / util.f
	constrain()

def constrain():
	global x0, y0
	from . import state
	d = math.sqrt(x0 ** 2 + y0 ** 2)
	if d > state.Rlevel:
		x0 *= state.Rlevel / d
		y0 *= state.Rlevel / d

def drawoverlay(alpha = 0.8, color = (0, 0, 0)):
	overlay = pygame.Surface(screen.get_size()).convert_alpha()
	overlay.fill((color[0], color[1], color[2], int(alpha * 255)))
	screen.blit(overlay, (0, 0))

def drawblob(blobspec, color = None, ocolor = None):
	hillspec = []
	for x, y, r, h in blobspec:
		x, y = screenpos((x, y))
		r = screenlength(r)
		hillspec.append((x, y, r, h))
	blob.drawcell(screen, hillspec, color = color, ocolor = ocolor)

def drawiris(R):
	iris = screen.copy()
	iris.fill((255, 255, 255))
	pygame.draw.circle(iris, (0, 0, 0), screenpos((0, 0)), screenlength(R))
	screen.blit(iris, (0, 0), None, pygame.BLEND_RGB_SUB)

def screenpos(p):
	x, y = p
	return F([
		854 / 2 + Z * (x - x0),
		480 / 2 + Z * -(y - y0),
	])

def gamepos(p):
	x, y = p
	return (
		x0 + (x - sx / 2) / Z / util.f,
		y0 - (y - sy / 2) / Z / util.f,
	)

def screenlength(r):
	return F(r * Z)


