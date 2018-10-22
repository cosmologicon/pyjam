import math
from OpenGL.GL import *
from OpenGL.GLU import *
from . import state

def init():
	global quadric
	quadric = gluNewQuadric()
	gluQuadricNormals(quadric, GLU_SMOOTH)
	gluQuadricTexture(quadric, GL_TRUE)

def drawsphere(r = 1):
	gluSphere(quadric, r, 10, 10)

def drawcircle(center, r, axis, color):
	# note: axis doesn't work - all horizontal circles for now
	glPushMatrix()
	glColor4f(*color)
	glTranslate(*center)
	gluDisk(quadric, 0.95 * r, 1.05 * r, 10, 10)
	glPopMatrix()

def drawcylinder(p0, r, h, color):
	glPushMatrix()
	glColor4f(*color)
	glTranslate(*p0)
	gluCylinder(quadric, r, r, h, 10, 1)
	glPopMatrix()
	

# TODO: use the imported fish model instead of a sphere. Don't worry about angle.
def drawyou():
	glPushMatrix()
	glColor4f(0.8, 0.5, 0, 1)
	glTranslate(*state.you.pos)
	angle = 20 * math.sin(state.you.Tswim * math.tau) - math.degrees(state.you.heading)
	glRotate(angle, 0, 0, 1)
	glScale(0.4, 1, 0.7)
	drawsphere()
	glPopMatrix()

# Placeholder - for now everything's spheres
def drawobj(obj):
	glPushMatrix()
	glColor4f(*(list(obj.color) + [1]))
	glTranslate(*obj.pos)
	drawsphere(obj.r)
	glPopMatrix()

