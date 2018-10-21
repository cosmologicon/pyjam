from OpenGL.GL import *

def drawwater():
	glColor4f(0, 0, 1, 0.3)
	glBegin(GL_QUADS)
	for dx, dy in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
		glVertex(dx * 4, dy * 10, 0)
	glEnd()
