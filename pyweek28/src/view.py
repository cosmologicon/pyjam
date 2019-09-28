# View coordinates: Pygame position in pixels
#   (xV, yV) = (0, 0) is top left, (pview.w, pview.h) is bottom right.
# World coordinates: fixed 3-D position of an object in the game world in units of krelmars (km).
#   (xW, yW) = (0, 0) is the central axis of the elevator.
#   The positive xW axis points East.
#   The positive yW axis points North.
#   zW = 0 at the bottom of the elevator.
#   zW = state.top at the top of the elevator.
#   Sometimes we drop the suffix: z = zW, since this is the only coordinate system with a z.

# Game coordinates: position in the main view window in units of krelmars (km).
#   This is an intermediate coordinate system, between world and view, used for graphical effects.
#   It's silimar to game coordinates but it's 2-d with the rotation taken into account.
#   xG = 0 at the center of the elevator, with positive xG to the right (from the camera's point of
#      view).
#   yG = 0 at the surface, with positive yG going up. i.e. yG = zW.

from __future__ import division
import pygame, math
from . import settings, pview, state
from .pview import T

# A is an angle around the central axis, in units of 1/8th of a rotation clockwise starting at North.
# A is in the range [0, 8) and wraps around so all calculations on angles are done mod 8.
Anames = "N", "NE", "E", "SE", "S", "SW", "W", "NW"

# Current height of the camera.
zW0 = 0
# Current size of a game unit in baseline pixels (still need to apply T to get to view coordinates)
zoom = 60
# Current angle of the camera. This is the *position* of the camera with respect to the elevator,
# and is 180 degrees off from the *direction* of the camera. So A = 0 means the camera is positioned
# on the North side of the elevator, looking South.
A = 0


def visible(z, dz = 0):
	return abs(z - zW0) < pview.centerx / zoom + dz


# Camera mode can be one of the following:
cmode = "z"

# "z": In this mode, the camera will soft approach to targetz and then remain stationary.
targetz = 0  # Where the camera wants to be
ftargetz = 0  # Approach factor, increases in time to allow for a slightly slower start.
def updatecamera_z(dt):
	global targetz, ftargetz, zW0, zoom
	dt *= math.exp(state.progress.missions / 20)
	ftargetz += dt
	f = 50 * ftargetz ** 3
	newz = math.softapproach(zW0, targetz, f * dt, dymin = 0.01)
	# TODO: This is supposed to give a sense of pulling back as the camera pans, but I'm not sure it
	# comes across. Try it again once the graphics are more in place.
	# zoom = 60 / (1 + 0.001 * abs(zW0 - newz) / dt)
	zW0 = newz
def seek_z(zW):
	global cmode, targetz, ftargetz
	cmode = "z"
	targetz = zW
	ftargetz = 0
	
# "car": In this mode, the camera will soft approach a car, matching its speed, and will track it
# thereafter.
targetcar = None
ftargetcar = 0
def updatecamera_car(dt):
	global ftargetcar, zW0
	dt *= math.exp(state.progress.missions / 20)
	ftargetcar = math.clamp(ftargetcar + 0.8 * dt, 0, 1)
	f = math.ease(math.ease(ftargetcar))
	zW0 = math.mix(targetcarstart, targetcar.z, f)

def seek_car(car):
	global cmode, targetcar, ftargetcar, targetcarstart
	cmode = "car"
	targetcar = car
	ftargetcar = 0
	targetcarstart = zW0

# Target angle for the camera. Should always be an integer.
# For now, angles are tracked independently from camera z-position.
targetA = 0
# Step left/right around the elevator by the given amount.
def rotate(dA):
	global targetA
	targetA = (targetA + dA) % 8
def rotateto(A):
	rotate(dA(A, targetA))


def init():
	pview.set_mode(settings.resolution)
	pygame.display.set_caption(settings.gamename)

def think(dt):
	global A
	if cmode == "z":
		updatecamera_z(dt)
	if cmode == "car":
		updatecamera_car(dt)

	A = Aapproach(A, targetA, 10 * dt)
	

def gametoview(pG):
	xG, yG = pG
	xG0, yG0 = 0, zW0
	xV = T(pview.centerx0 + (xG - xG0) * zoom)
	yV = T(pview.centery0 - (yG - yG0) * zoom)
	return xV, yV

# TODO: implement viewtogame


# Return ((xG, yG), dG), where dG is a depth coordinate, equal to 0 in the plane of the elevator,
# and positive when closer to the camera than the elevator is.
def worldtogame(pW):
	xW, yW, zW = pW
	xGneg, dG = math.R(A/8 * math.tau, (xW, yW))
	yG = zW
	xG = -xGneg
	return (xG, yG), dG

def worldtoview(pW):
	pG, dG = worldtogame(pW)
	return gametoview(pG)

# viewing angles A are wrapped between 0 and 8. This returns the difference A0 - A1 (mod 8) such
# that the value is in the range [-4, 4).
def dA(A0, A1):
	return (A0 - A1 + 4) % 8 - 4

# approach function that takes the shortest distance wrapping around between 0 and 1.
# e.g. if you're at A0 = 7 and you want to approach A1 = 0, this will increase rather than decrease.
def Aapproach(A0, A1, Astep):
	return (A1 - math.softapproach(dA(A1, A0), 0, Astep, dymin = 0.01)) % 8
	

