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
	y0 = state.you.pos.y
	glBegin(GL_QUADS)
	for dx, dy in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
		glVertex(dx * 4, y0 + dy * 100, 0)
	glEnd()
	# Fixed barriers
	y0 = 10 * round(y0 / 10)
	glColor4f(0.8, 0.8, 0.8, 1)
	for dy in range(-10, 10):
		for x in (-4, 4):
			glPushMatrix()
			glTranslate(x, y0 + 10 * dy, 0)
			drawsphere(0.3)
			glPopMatrix()


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
	
