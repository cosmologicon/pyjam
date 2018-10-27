from __future__ import division
import datetime, math
import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, state, graphics

screen = None

# Camera conventions (all angles in degrees):
#   Rvantage = distance from camera to vantage point
#   theta = 0: directly overhead
#   theta = 90: from the side
#   phi = 0: camera faces north
#   phi = 90: camera faces west
#   eta = 0: up for the camera is in the z direction
#   eta > 0: up is tilted to the right (so the horizon goes from lower left to upper right
#   eta < 0: up is tilted to the left
#   In addition there is a vector atilt that rotates the entire setup based on flow of the current
#   section (slope or curved).

# Hack to allow some "global" variables in this method.
class self:
	camera = pygame.math.Vector3(0, 0, 0)
	vantage = pygame.math.Vector3(1, 0, 0)
	up = pygame.math.Vector3(0, 0, 1)
	# Countdown timer of how long the camera should lag in catching up to the player
	tosnap = 0

	# Current mouse settings of gamma and phi
	mgamma = 40
	mphi = 0
	# Current actual settings
	gamma = 40
	phi = 0
	atilt = Vector3(0, 0, 0)
	Rvantage = 20

	# Currently in rapid mode
	rapid = False

	# Whether we're in "f"-mode (as in fixed), i.e. in the northwest puzzle
	fmode = False
	fcamera = Vector3(0, 0, 0)
	# Whether we're in "b"-mode (as in final boss), semifixed
	bmode = False
	bphi = 0

def init():
	global screen
	flags = pygame.DOUBLEBUF | pygame.OPENGL
	if settings.fullscreen:
		flags |= pygame.FULLSCREEN
	screen = pygame.display.set_mode(settings.resolution, flags)
	grabmouse(False)

def clear(color = (0, 0, 0, 1)):
	glClearColor(*color)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def addsnap(dt):
	self.tosnap += dt

def grabmouse(snap = False):
	if settings.manualcamera:
		pygame.mouse.set_visible(False)
		pygame.event.set_grab(True)
	else:
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(False)
	if snap:
		addsnap(0.2)

def think(dt, dmx, dmy):
	self.tosnap = max(self.tosnap - dt, 0)

	if settings.manualcamera:
		self.mgamma = math.clamp(self.mgamma - 100 * dmy, 5, 85)
		self.mphi -= 100 * dmx

	camera = 1 * state.you.pos
	atilt = state.you.section.atilt(state.you)
	Rvantage = 20
	gamma = 55
	phi = -math.degrees(state.you.heading)

	if state.you.section.fmode is None:
		pass
	elif state.you.section.fmode:
		if not self.fmode:
			self.fmode = True
			self.tosnap = 1
	else:
		if self.fmode:
			self.fmode = False
			self.tosnap = 1

	if state.you.section.bmode is None:
		pass
	elif state.you.section.bmode:
		if not self.bmode:
			self.bmode = True
			self.tosnap = 1
	else:
		if self.bmode:
			self.bmode = False
			self.tosnap = 0.5

	if self.fmode:
		if state.you.section.label == "pool":
			self.fcamera = state.you.section.pos * 1	
		camera = math.softapproach(self.camera, self.fcamera, 3 * dt)
		phi = 0
		gamma = 40
		Rvantage = math.softapproach(self.Rvantage, 40, 3 * dt)

	if self.bmode:
		camera = math.softapproach(self.camera, state.you.section.pos, 3 * dt)
		d = state.you.pos - state.you.section.pos
		d.z = 0
		
		if d.x == 0 and d.y == 0:
			kappa = 0
		else:
			kappa = math.degrees(math.atan2(d.y, d.x)) - 90
		dphi = math.zmod(self.bphi - kappa, 360)
		if 0 < dphi < 70:
			self.bphi += 70 - dphi
		elif -70 < dphi < 0:
			self.bphi += -70 - dphi
		phi = self.bphi
		gamma = 55
		Rvantage = math.softapproach(self.Rvantage, 45, 3 * dt)

	if state.you.section.rapid > 1:
		if not self.rapid:
			self.tosnap = 1
			self.rapid = True
		Rvantage = 12
		gamma = 68
	else:
		if self.rapid:
			self.tosnap = 1
			self.rapid = False

	# f is approximately dt / self.tosnap for large values of self.tosnap
	# rapidly approaches 1 as self.tosnap goes to 0
	fsnap = 1 - math.exp(-dt / self.tosnap) if self.tosnap > 0 else 1

	if settings.manualcamera:
		gamma = self.mgamma
		phi = self.mphi

	self.gamma = math.mix(self.gamma, gamma, fsnap)
	self.phi += fsnap * math.zmod(phi - self.phi, 360)
	if fsnap == 0:
		self.phi = phi
	self.Rvantage = math.mix(self.Rvantage, Rvantage, fsnap)
	self.atilt = math.mix(self.atilt, atilt, 2 * dt)
	
	if not settings.manualcamera:
		self.mgamma = self.gamma
		self.mphi = self.phi

	theta = self.gamma
	uvantage = Vector3(0, 0, 1).rotate_x(theta).rotate_z(self.phi)
	
	dtilt = self.atilt.length()
	utilt = self.atilt.normalize() if dtilt else Vector3(0, 0, 1)
	self.camera = camera
	self.vantage = self.camera + self.Rvantage * uvantage.rotate(dtilt, utilt)
	self.up = Vector3(0, 0, 1).rotate_z(self.phi).rotate(dtilt, utilt)


# Set up camera perspective and settings for drawing game entities
def look():
	
	# cycle animation variables
	state.animation.cycle()
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	w, h = screen.get_size()
	fov = 45
	gluPerspective(fov, w / h, 0.1, 1000.0)
	args = list(self.vantage) + list(self.camera) + list(self.up)
	gluLookAt(*args)
	
	glMatrixMode(GL_MODELVIEW)
	glEnable(GL_DEPTH_TEST)
	glDepthMask(GL_TRUE)

def maplook():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	w, h = screen.get_size()
	glScale(1 / 150, 1 / 150 * w / h, -1 / 1000)


def screenshot():
	# TODO: get screenshot working
	filename = datetime.datetime.now().strftime("screenshot-%Y%m%d%H%M%S.png")
	w, h = screen.get_size()
	data = glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
	surf = pygame.Surface((w, h)).convert_alpha()
	arr = pygame.surfarray.pixels3d(surf)

