from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
import numpy, pygame, math

from . import pview, world, view, state


def prand(seed):
	return hash(seed) % 1234567 * math.phi % 1

def iP(ix, iy, iz, seed):
	return -1 + 2 * prand((ix, iy, iz, seed))

def P(x, y, z, seed):
	value = 0
	ix0, rx0 = divmod(x, 1)
	iy0, ry0 = divmod(y, 1)
	iz0, rz0 = divmod(z, 1)
	for ix, rx in [(ix0, 1 - rx0), (ix0 + 1, rx0)]:
		for iy, ry in [(iy0, 1 - ry0), (iy0 + 1, ry0)]:
			for iz, rz in [(iz0, 1 - rz0), (iz0 + 1, rz0)]:
				value += math.ease(rx) * math.ease(ry) * math.ease(rz) * iP(ix, iy, iz, seed)
	return value


def noiseat(p, scales, a=1, j=0, b=0.3, seed=0):
	fs = math.norm([scale ** b for scale in scales], a)
	x, y, z = p
	n = 0
	for i, (f, scale) in enumerate(zip(fs, scales)):
		n += f * P(x / scale, y / scale, z / scale, (i, scale, seed))
	return n


def utweak(pos, dh = 0.01):
	h = 1 + noiseat(pos, [0.1, 0.07, 0.04], a = 0.01)
	return math.norm(pos, h * world.R)

def acolor(h):
	if h < 0:
		return math.smoothfadebetween(h, -10, (0, 0, 0), 0, (0.5, 0.3, 0))
	if h < 0.5:
		return math.smoothfadebetween(h, 0, (0.5, 0.3, 0), 0.5, (0.2, 0.5, 0.2))
	return math.smoothfadebetween(h, 0.5, (0.2, 0.5, 0.2), 1, (0.7, 0.7, 0.7))

def isize(ispec, theta):
	s = 1
	for ds, n, jtheta0 in ispec:
		s += ds * math.sin(jtheta0 + n * theta)
	return s


def capwrap(s, x, y, z):
	r = math.length([x, y])
	z, r = math.CS(s * r / world.R, z + world.R)
	x, y = math.norm([x, y], r)
	return x, y, z - world.R
	

def iring(r0, z0, r1, z1, ispec, ntheta, jtheta0):
#	z0, r0 = math.CS(r0 / world.R, world.R + z0)
#	z1, r1 = math.CS(r1 / world.R, world.R + z1)
#	z0, z1 = z0 - world.R, z1 - world.R
	CS0 = math.CSround(ntheta, r = r0, jtheta0 = jtheta0)
	size0 = [isize(ispec, (jtheta0 + jtheta) / ntheta * math.tau) for jtheta in range(ntheta)]
	CS1 = math.CSround(ntheta, r = r1, jtheta0 = jtheta0 - 0.5)
	size1 = [isize(ispec, (jtheta0 - 0.5 + jtheta) / ntheta * math.tau) for jtheta in range(ntheta)]
	CS2 = CS1[1:] + CS1[:1]
	size2 = size1[1:] + size1[:1]
	for (x0, y0), (x1, y1), (x2, y2), s0, s1, s2 in zip(CS0, CS1, CS2, size0, size1, size2):
		p0 = capwrap(s0, x0, y0, z0)
		p1 = capwrap(s1, x1, y1, z1)
		p2 = capwrap(s2, x2, y2, z1)
#		print(r0, s0, x0, y0, z0, p0)
		if r1 < r0:
			yield p0, p2, p1
		else:
			yield p0, p1, p2

def island(rs, zs, ispec, ntheta = 20):
	for n in range(len(rs)):
		jtheta0 = 0.5 if n % 2 else 0
		if n < len(rs) - 1:
			yield from iring(rs[n], zs[n], rs[n+1], zs[n+1], ispec, ntheta, jtheta0)
		if n > 1:
			yield from iring(rs[n], zs[n], rs[n-1], zs[n-1], ispec, ntheta, jtheta0)


# https://en.wikibooks.org/wiki/GLSL_Programming/Applying_Matrix_Transformations#Built-In_Matrix_Transformations
sky_vshader = """
#version 120
attribute vec3 p;
varying vec3 tcoord;
void main() {
	gl_Position = (gl_ModelViewMatrix * p).xyww;
	tcoord = p;
}
"""
sky_fshader = """
#version 120
varying vec3 tcoord;
void main() {
	gl_FragColor = vec4(1.0, 0.01 * tcoord.x, 0.0, 1.0);
}
"""

class sky:
	pass


class lists:
	islands = {}

def init():
	if False:
		vshader = shaders.compileShader(sky_vshader, GL_VERTEX_SHADER)
		fshader = shaders.compileShader(sky_fshader, GL_FRAGMENT_SHADER)
		sky.shader = shaders.compileProgram(vshader, fshader)
		sky.locations = {
			"p": glGetAttribLocation(_shader, "p"),
		}
		sky.pdata = numpy.array([-1, -1, -1, -1, 1, -1, ], numpy.float32)


	sdata = list(world.usphere(4))
#	glEnable(GL_NORMALIZE)


	lists.you = glGenLists(1)
	glNewList(lists.you, GL_COMPILE)
	glBegin(GL_TRIANGLES)
#	glColor3fv((1, 0.7, 0.4))
	for face in world.usphere(1):
		for vertex in face:
			glVertex3fv(world.times(vertex, 3))
	glEnd()
	glEndList()

	lists.world = glGenLists(1)
	glNewList(lists.world, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in sdata:
		color = world.plus((0.5, 0.5, 0.5), math.norm(world.avg(*face), 0.5))
#		glColor3fv(color)
#		glNormal3fv()
		for vertex in face:
			v = utweak(vertex)
			glColor3fv(acolor(math.length(v) / world.R))
#			glNormal3fv(n)
			glVertex3fv(v)
#			glNormal3fv(vertex)
#			glVertex3fv(vertex)
	glEnd()
	glEndList()

	lists.moonrod = glGenLists(1)
	glNewList(lists.moonrod, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in island([0, 2, 4, 6], [12, 10, 0, -20], [], 5):
		f = 0.8 + 0.2 * math.dot(world.normal(face), math.norm([1, 1, 1]))
		glColor3fv(world.times((0.3, 0.6, 0.5), f))
		for vertex in face:
			glVertex3fv(vertex)
	glEnd()
	glEndList()



	lists.water = glGenLists(1)
	glNewList(lists.water, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in sdata:
		for vertex in face:
			f = 0.5 + 0.3 * noiseat(vertex, [0.2, 0.07, 0.4])
			color0 = 0, 0.2, 0.4
			color1 = 0, 0.4, 0.4
#			color1 = world.linsum([1, 1, 1], 0.5, vertex, 0.5)
#			f = 1
			glColor3fv(math.mix(color0, color1, f))
			glVertex3fv(world.times(vertex, world.R))
	glEnd()
	glEndList()


	lists.moon = glGenLists(1)
	glNewList(lists.moon, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in sdata:
		for vertex in face:
			c = 0.3 + 0.05 * noiseat(vertex, [0.4, 0.3, 0.14], seed="moon")
			glColor4f(c, c, c, 1)
			glVertex3fv(world.times(vertex, 0.5 * world.R))
	glEnd()
	glEndList()

	lists.wake = glGenLists(1)
	glNewList(lists.wake, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	glColor3f(0.9, 0.9, 1)
	ispec = [(0.014, 13, 0.1), (0.012, 21, 0.2), (0.01, 34, 0.3)]
	for face in iring(0.9, 0, 1, 0, ispec, 100, 0):
		for vertex in face:
			glVertex3fv(vertex)
	for face in iring(1, 0, 0.9, 0, ispec, 100, 0.5):
		for vertex in face:
			glVertex3fv(vertex)
	glColor3f(0.2, 0.4, 0.7)
	for face in iring(0, 0, 0.9, 0, ispec, 100, 0.5):
		for vertex in face:
			glVertex3fv(vertex)
	glEnd()
	glEndList()

def renderisland(name, ispec, R):
	lists.islands[name] = glGenLists(1)
	glNewList(lists.islands[name], GL_COMPILE)
	glBegin(GL_TRIANGLES)
	# ispec = [(0.1, 4, 0.1), (0.07, 7, 0.8), (0.05, 8, 0.4)]
	rs = [r * R / 20 for r in [0, 2, 4, 6, 9, 14, 18, 20, 22]]
	zs = [z * 2 for z in [3, 2.9, 2.7, 2.6, 2.5, 2, 1, 0, -10]]
	for face in island(rs, zs, ispec, 50):
		for vertex in face:
			x, y, z = vertex
			h = math.length([x, y, z + world.R]) - world.R
			h = h / 6 + 0.12 * noiseat(vertex, [10, 5, 2, 1])
			f = 0.8 + 0.2 * noiseat(vertex, [19, 13, 8], seed="shade")
			glColor3fv(world.times(acolor(h), f))
			glVertex3fv(vertex)
	glEnd()
	glEndList()



def draw():
	glPushMatrix()

	glFrontFace(GL_CCW)
	glEnable(GL_CULL_FACE)
	glCullFace(GL_BACK)

	glEnable(GL_DEPTH_TEST)
	glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1))
#	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0, 1, 0, 1))
#	glLightfv(GL_LIGHT0, GL_POSITION, (-10, 8, 10, 1))
#	glEnable(GL_LIGHT0)
#	glEnable(GL_LIGHTING)
	glDisable(GL_TEXTURE_2D)
#	glRotatef(90 * 0.001 * pygame.time.get_ticks(), 1, 1, 1)

#	glCallList(lists.world)


	for island in state.islands:
		glPushMatrix()
		island.orient()
		glCallList(lists.islands[island.name])
		glPopMatrix()

#	glPushMatrix()
#	glTranslate(0, 0, world.R)
#	glCallList(lists.island)
#	glPopMatrix()



	glPushMatrix()
	f = 1 + 0.001 * (0.5 * math.cycle(0.3 * 0.001 * pygame.time.get_ticks()) - 0.5)
	glScale(f, f, f)
	glTranslate(*world.times(state.rmoon, state.tide))
	f, l, u = world.wspot
#	print(world.wspot)
	glMultMatrixf([*f,0,  *l,0,  *u,0,  0,0,0,1])
	glCallList(lists.water)
	glPopMatrix()

	glPushMatrix()
	state.moonrod.orient()
	glCallList(lists.moonrod)
	glPopMatrix()


	glPushMatrix()
	state.you.orient()
	color = [0.8, 0.4, 0.0] if state.islands[-1].distout(state.you.up) > 0 else [0.8, 0.8, 0.8]
	glColor3fv(color)
	glCallList(lists.you)
	glDisable(GL_CULL_FACE)
	d = math.fadebetween(math.length(state.you.v), 0, 1, 100, 10)
	glPushMatrix()
	glTranslate(-4, 6, -3)
	glRotate(135, 0, 0, 1)
	glRotatef(105, 1, 0, 0)
	glScale(d, d, d)
	glRotate(-200 * 0.001 * pygame.time.get_ticks() % 360, 0, 0, 1)
	glCallList(lists.wake)
	glPopMatrix()
	glPushMatrix()
	glTranslate(-4, -6, -3)
	glRotate(-135, 0, 0, 1)
	glRotatef(75, 1, 0, 0)
	glScale(d, d, d)
	glRotate(-200 * 0.001 * pygame.time.get_ticks() % 360 + 65, 0, 0, 1)
	glCallList(lists.wake)
	glPopMatrix()
	glEnable(GL_CULL_FACE)
	glPopMatrix()
	

	glEnable(GL_BLEND)
	glBlendColor(1, 0, 0, view.moonalpha())
	glBlendFunc(GL_CONSTANT_ALPHA, GL_ONE_MINUS_CONSTANT_ALPHA)
	glPushMatrix()
	glTranslate(*world.times(state.rmoon, 1.6 * world.R))
	glCallList(lists.moon)
	glPopMatrix()
	glDisable(GL_BLEND)

	glPopMatrix()


