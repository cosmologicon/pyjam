from __future__ import division
import pygame, math, os, datetime
from . import settings, util

screen = None
sx, sy = None, None
x0, y0 = 0, 0
target = None
Z = 5

def init():
	setwindow()
	pygame.display.set_caption(settings.gamename + (" [DEBUG MODE]" if settings.DEBUG else ""))

def setwindow():
	global screen, sx, sy
	if settings.fullscreen:
		sx, sy = max(pygame.display.list_modes())
		screen = pygame.display.set_mode((sx, sy), pygame.FULLSCREEN)
	else:
		sy = settings.resolution
		sx = int(math.ceil(16 / 9 * sy))
		screen = pygame.display.set_mode((sx, sy))
	util.f = sy / settings.resolution0

def screenshot():
	if not os.path.exists("screenshots"):
		os.mkdir("screenshots")
	filename = datetime.datetime.now().strftime("screenshots/screenshot-%Y%m%d%H%M%S.png")
	try:
		pygame.image.save(screen, filename)
	except pygame.error:
		filename = datetime.datetime.now().strftime("screenshots/screenshot-%Y%m%d%H%M%S.bmp")
		pygame.image.save(screen, filename)

def togglefullscreen():
	settings.fullscreen = not settings.fullscreen
	setwindow()

# center of screen
px0 = settings.resolution0 * (16 / 9) / 2
py0 = settings.resolution0 / 2
fy = settings.yscalefactor
fz = math.sqrt(1 - fy ** 2)
def worldtoscreen(x, y, z):
	px = px0 + (x - x0) * Z
	py = py0 - (fy * (y - y0) + fz * z) * Z
	return util.F(px, py)
def screentoworld(px, py):  # at z = 0
	return [
		x0 + (px / util.f - px0) / Z,
		y0 - (py / util.f - py0) / (fy * Z),
	]

def snapto(obj):
	snaptopos(obj.x, obj.y, obj.z)
def snaptopos(x, y, z):
	global x0, y0
	x0 = x
	y0 = y + z * fz / fy
def targetpos(x, y, z = 0):
	global target
	target = x, y + z * fz / fy
def think(dt):
	global target, x0, y0
	if target is not None:
		tx, ty = target
		dx, dy = tx - x0, ty - y0
		if dx ** 2 + dy ** 2 < 0.1:
			x0, y0 = target
			target = None
		else:
			f = 1 - math.exp(-8 * dt)
			x0 += f * dx
			y0 += f * dy
def scoot(dx, dy):
	global x0, y0
	x0 += dx
	y0 += dy


def getstate():
	return x0, y0

def setstate(obj):
	global x0, y0
	x0, y0 = obj


