# View coordinates: Pygame position in pixels
#   (xV, yV) = (0, 0) is top left, (pview.w, pview.h) is bottom right.
# Game coordinates: position in the main view window in units of krelmars (km).
#   xG = 0 at the center of the elevator, with positive xG to the right.
#   yG = 0 at the surface, with positive yG going up.
# A is the viewing angle, going from 0 to 1 and wrapping around.
# A = 0 means facing North, i.e. the camera is South of the elevator.
# A = 1/8 means facing Northeast, i.e. the camera is Southwest of the elevator.
# This can be a little counterintuitive, but if you step left, that moves you clockwise around the
# elevator, e.g. from South to Southwest.
# Note that xG refers to the viewing plane from the player's perspective. This means that an
# object's xG coordinate changes as you step around the elevator.
# World coordinates: fixed 3-D position of an object in the game world in units of km. Similar to
#   game coordinates but different when you take rotation into account. (xW, yW) = (0, 0) is the
#   central axis of the elevator. zW = 0 at the bottom.


from __future__ import division
import pygame, math
from . import settings, pview
from .pview import T

# Current center of the screen in game coordinates. xG0 will probably always be 0.
xG0, yG0 = 0, 0
# Current size of a game unit in baseline pixels (still need to apply T to get to view coordinates)
zoom = 100
# Current viewing angle
A = 0


# TODO: make the camera approach functions faster as the game progresses.

# Camera mode can be one of the following:
cmode = "y"

# "y": In this mode, the camera will soft approach to targetyG and then remain stationary.
targetyG = 0  # Where the camera wants to be
ftargetyG = 0  # Approach factor, increases in time to allow for a slightly slower start.
def updatecamera_y(dt):
	global targetyG, ftargetyG, yG0
	ftargetyG += dt
	f = 100 * ftargetyG ** 3
	newyG0 = math.softapproach(yG0, targetyG, f * dt, dymin = 0.01)
	# TODO: This is supposed to give a sense of pulling back as the camera pans, but I'm not sure it
	# comes across. Try it again once the graphics are more in place.
	# zoom = 100 / (1 + 0.001 * abs(yG0 - newyG0) / dt)
	yG0 = newyG0
def seek_y(yG):
	global cmode, targetyG, ftargetyG
	cmode = "y"
	targetyG = yG
	ftargetyG = 0
	
# "car": In this mode, the camera will soft approach a car, matching its speed, and will track it
# thereafter.
targetcar = None
ftargetcar = 0
def updatecamera_car(dt):
	global ftargetcar, yG0
	ftargetcar = math.clamp(ftargetcar + 2 * dt, 0, 1)
	f = math.ease(math.ease(ftargetcar))
	yG0 = math.mix(targetcarstart, targetcar.yG, f)

def seek_car(car):
	global cmode, targetcar, ftargetcar, targetcarstart
	cmode = "car"
	targetcar = car
	ftargetcar = 0
	targetcarstart = yG0

# For now, angles are tracked independently from camera y-position.
targetA = 0
def rotate(dA):
	global targetA
	targetA = (round(targetA * 8) + dA) % 8 / 8


def init():
	pview.set_mode(settings.resolution)
	pygame.display.set_caption(settings.gamename)

def think(dt):
	global A
	if cmode == "y":
		updatecamera_y(dt)
	if cmode == "car":
		updatecamera_car(dt)

	A = Aapproach(A, targetA, 10 * dt)
	

def gametoview(pG):
	xG, yG = pG
	xV = T(pview.centerx0 + (xG - xG0) * zoom)
	yV = T(pview.centery0 - (yG - yG0) * zoom)
	return xV, yV

# TODO: implement viewtogame


# Return ((xG, yG), dG), where dG is a depth coordinate, equal to 0 in the plane of the elevator,
# and positive when closer to the camera than the elevator is.
def worldtogame(pW):
	xW, yW, zW = pW
	xG, dGneg = math.R(A * math.tau, (xW, yW))
	yG = zW
	dG = -dGneg
	return (xG, yG), dG

# viewing angles A are wrapped between 0 and 1. This returns the difference A0 - A1 (mod 1) such
# that the value is between -1/2 and +1/2.
def dA(A0, A1):
	return (A0 - A1 + 1/2) % 1 - 1/2

# approach function that takes the shortest distance wrapping around between 0 and 1.
# e.g. if you're at A0 = 7/8 and you want to approach A1 = 0, this will increase rather than decrease.
def Aapproach(A0, A1, Astep):
	return (A1 - math.softapproach(dA(A1, A0), 0, Astep, dymin = 0.001)) % 1
	

