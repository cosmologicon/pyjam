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

def drawwater():
	glColor4f(0, 0, 1, 0.3)
	y0 = 10 * round(state.you.pos.y / 10)
	glBegin(GL_QUADS)
	for dx, dy in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
		glVertex(dx * 4, y0 + dy * 10, 0)
	glEnd()

def drawyou():
	glColor4f(0.8, 0.8, 0, 1)
	glTranslate(*state.you.pos)
	glRotate(20 * math.sin(state.you.Tswim * math.tau), 0, 0, 1)
	glScale(0.4, 1, 0.7)
	drawsphere()

