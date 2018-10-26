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
#   theta = gamma - kappa
#   gamma is the baseline tilt due to the vantage point looking down on the object.
#   kappa is additional tilt due to the camera position being on a slope.
#   phi = 0: camera faces north
#   phi = 90: camera faces west
#   eta = 0: up for the camera is in the z direction
#   eta > 0: up is tilted to the right (so the horizon goes from lower left to upper right
#   eta < 0: up is tilted to the left

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
	eta = 0

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
	# f is approximately dt / self.tosnap for large values of self.tosnap
	# rapidly approaches 1 as self.tosnap goes to 0
	fsnap = 1 - math.exp(-dt / self.tosnap) if self.tosnap > 0 else 1

	if settings.manualcamera:
		self.mgamma = math.clamp(self.mgamma - 100 * dmy, 5, 85)
		self.mphi -= 100 * dmx


	camera = 1 * state.you.pos
	ytilt, xtilt = state.you.section.atilt(state.you)
	Rvantage = 20
	gamma = 55
	phi = -math.degrees(state.you.heading)

	if settings.manualcamera:
		gamma = self.mgamma
		phi = self.mphi

	self.gamma = math.mix(self.gamma, gamma, fsnap)
	self.phi = math.mix(self.phi, phi, fsnap)

	if not settings.manualcamera:
		self.mgamma = self.gamma
		self.mphi = self.phi

	kappa = -ytilt
	eta = xtilt
	theta = self.gamma - kappa
	uvantage = Vector3(0, 0, 1).rotate_x(theta).rotate_z(self.phi)
	
	self.camera = camera
	self.vantage = camera + Rvantage * uvantage
	self.up = Vector3(0, 0, 1).rotate_y(eta).rotate_z(self.phi)

	

#	ytilt, xtilt = state.you.section.atilt(state.you)
#	self.xtilt = math.softapproach(self.xtilt, xtilt, 4 * dt)
#	self.ytilt = math.softapproach(self.ytilt, ytilt, 4 * dt)
	# Hard-coded (for now) perspective change when you go east.
#	back = math.smoothfadebetween(state.you.pos.x, 50, 20, 70, 10)
#	up = math.smoothfadebetween(state.you.pos.x, 50, 16, 70, 4)
#	face = state.you.face.normalize()
#	if state.you.section.label == "pool" and state.you.section.final:
#		face = self.finalface
#		camera = state.you.section.pos
#		back = 25
#		up = 15
#		try:
#			d0 = (state.you.pos - camera).normalize()
#			z = d0.cross(self.finalface).normalize()
#			d1 = z.cross(d0).normalize()
#			fturn = self.finalface.rotate(-50, z)
#			if fturn.dot(d0) > fturn.dot(d1) > 0:
#				fnew = (d0 + d1).normalize().rotate(50, z).normalize()
#				self.finalface = math.softapproach(self.finalface, fnew, 2 * dt)
#				face = self.finalface
#		except ValueError:
#			pass
#	else:
#		self.finalface = face
#	right = face.cross(pygame.math.Vector3(0, 0, 1)).normalize()
#	self.up = pygame.math.Vector3(0, 0, up)
#	self.up = self.up.rotate(self.xtilt, face)
#	self.up = self.up.rotate(self.ytilt, right)
#	print(self.up, face, xtilt, right)
#	face = face.rotate(self.xtilt, face)
#	face = face.rotate(self.ytilt, right)
#	print(self.xtilt, self.ytilt, face, self.up)
#	vantage = camera - back * face + self.up
#	self.camera += fsnap * (camera - self.camera)
#	self.vantage += fsnap * (vantage - self.vantage)

# Set up camera perspective and settings for drawing game entities
def look():
	
	# cycle animation variables
	graphics.animation.cycle()
	
	# TODO: get lighting working
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	# TODO: probably don't need to center the player character
	# can we put it 3/4 of the way down the window?
	w, h = screen.get_size()
	fov = 45
	gluPerspective(fov, w / h, 0.1, 1000.0)
	args = list(self.vantage) + list(self.camera) + list(self.up)
	gluLookAt(*args)
	
	#glEnable(GL_BLEND)
	# TODO: get water transparency working
	#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	glMatrixMode(GL_MODELVIEW)
	glEnable(GL_DEPTH_TEST)
	glDepthMask(GL_TRUE)

def maplook():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	w, h = screen.get_size()
	glScale(1 / 140, 1 / 140 * w / h, -1 / 1000)


def screenshot():
	# TODO: get screenshot working
	filename = datetime.datetime.now().strftime("screenshot-%Y%m%d%H%M%S.png")
	w, h = screen.get_size()
	data = glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
	surf = pygame.Surface((w, h)).convert_alpha()
	arr = pygame.surfarray.pixels3d(surf)

