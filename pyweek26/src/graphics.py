import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from . import state

def init():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

def drawsphere(r = 1):
	glutSolidSphere(r, 10, 10)

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
	glColor4f(*obj.color, 1)
	glTranslate(*obj.pos)
	drawsphere(obj.r)
	glPopMatrix()
	
