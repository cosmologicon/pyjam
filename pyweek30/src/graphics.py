from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy, pygame, math

from . import pview, world


def utweak(pos, dn = 0.1, dh = 0.01):
	x, y, z = pos
	dx = (4.7 * x + 8.3 * y + 2.2 * z) % 1 - 0.5
	dy = (5.7 * x + 9.3 * y + 3.2 * z) % 1 - 0.5
	dz = (6.7 * x + 10.3 * y + 4.2 * z) % 1 - 0.5
	h = 1 + dh * (math.cycle(x + 2 * y + 3 * z + x * y) - 0.5)
	n = x + dn * dx, y + dn * dy, z + dn * dz
	return math.norm(n), math.norm(pos, h * world.R)

def init():
	global sdata, world_list, water_list
	sdata = list(world.usphere(5))
#	glEnable(GL_NORMALIZE)
	glFrontFace(GL_CCW)



	world_list = glGenLists(1)
	glNewList(world_list, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in sdata:
		color = world.plus((0.5, 0.5, 0.5), math.norm(world.avg(*face), 0.5))
		glColor3fv(color)
#		glNormal3fv()
		for vertex in face:
			n, v = utweak(vertex)
#			glNormal3fv(n)
			glVertex3fv(v)
#			glNormal3fv(vertex)
#			glVertex3fv(vertex)
	glEnd()
	glEndList()


	water_list = glGenLists(1)
	glNewList(water_list, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	glColor3fv((0, 0.2, 0.4))
	for face in sdata:
		for vertex in face:
			glVertex3fv(world.times(vertex, world.R))
	glEnd()
	glEndList()


def draw():
	glEnable(GL_DEPTH_TEST)
	glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1))
#	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0, 1, 0, 1))
#	glLightfv(GL_LIGHT0, GL_POSITION, (-10, 8, 10, 1))
#	glEnable(GL_LIGHT0)
#	glEnable(GL_LIGHTING)
	glDisable(GL_TEXTURE_2D)
#	glRotatef(90 * 0.001 * pygame.time.get_ticks(), 1, 1, 1)

	glCallList(world_list)
	f = 1 + 0.001 * 0.5 * math.cycle(0.001 * pygame.time.get_ticks())
	glScale(f, f, f)
	glCallList(water_list)



	glLoadIdentity()
	gluPerspective(45, pview.aspect, 0.1, 10 * world.R)
	gluLookAt(*world.getlookat())



