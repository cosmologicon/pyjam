from OpenGL.GL import *
from OpenGL.GLU import *
import numpy, pygame, math, random

from . import pview, world, view, state, settings


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

def shake(t, n = 1):
	return [n * noiseat([0.5, 0.5, t], [0.3, 0.1, 0.06, 0.04], seed=j) for j in range(3)]


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
		if r1 < r0:
			yield p0, p2, p1
		else:
			yield p0, p1, p2

def island(rs, zs, ispec, ntheta = 20):
	for n in range(len(rs)):
		jtheta0 = 0.5 if n % 2 else 0
		if n < len(rs) - 1:
			yield from iring(rs[n], zs[n], rs[n+1], zs[n+1], ispec, ntheta, jtheta0)
		if n > 0 and rs[n] > 0:
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

	lists.stars = glGenLists(1)
	glNewList(lists.stars, GL_COMPILE)
	glPointSize(1)
	glBegin(GL_POINTS)
	z0 = math.norm([1, 1, 1])
	z1 = math.norm([-1, 2, -3])
	for j in range(10):
		glColor3fv(math.mix([1, 1, 1], [0.5, 0.5, 0.5], j/9))
		for _ in range(3000):
			glVertex3fv(world.randomunit())
		for _ in range(1000):
			a = world.randomunit()
			a = world.plus(a, world.times(z0, -0.8 * math.dot(a, z0)))
			a = world.plus(a, world.times(z0, -0.8 * math.dot(a, z0)))
			glVertex3fv(math.norm(a))
		for _ in range(2000):
			a = world.randomunit()
			a = world.plus(a, world.times(z1, -0.94 * math.dot(a, z1)))
			glVertex3fv(math.norm(a))
	glEnd()
	glEndList()


	lists.you = glGenLists(1)
	glNewList(lists.you, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for v0, v1, v2 in world.usphere(2):
		f = math.dot(math.norm([1, 1, 1]), math.norm(world.cross(world.minus(v2, v0), world.minus(v1, v0))))
		glColor3fv(world.times([1, 1, 1], 0.6 + 0.2 * f))
		for x, y, z in (v0, v1, v2):
			x = 2 * x ** 4 if x > 0 else x
#			z = z * 2 - 0.3
			glVertex3fv(world.times((x, y, z), 4))
	for v0, v1, v2 in world.usphere(0):
		f = math.dot(math.norm([1, 1, 1]), math.norm(world.cross(world.minus(v2, v0), world.minus(v1, v0))))
		glColor3fv(world.times([1, 1, 1], 0.6 + 0.2 * f))
		for x, y, z in (v0, v1, v2):
			x, y, z = world.rot([0, 0, 1], (x, y, z), -0.3)
			x -= 2 * x ** 4 if x < 0 else 0
#			z = z * 2 - 0.3
			glVertex3fv(world.times((x, y - 2, z), 3))
	for v0, v1, v2 in world.usphere(0):
		f = math.dot(math.norm([1, 1, 1]), math.norm(world.cross(world.minus(v2, v0), world.minus(v1, v0))))
		glColor3fv(world.times([1, 1, 1], 0.6 + 0.2 * f))
		for x, y, z in (v0, v1, v2):
			x, y, z = world.rot([0, 0, 1], (x, y, z), 0.3)
			x -= 2 * x ** 4 if x < 0 else 0
#			z = z * 2 - 0.3
			glVertex3fv(world.times((x, y + 2, z), 3))
	glEnd()
	glEndList()

	if False:
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
	CSs = [math.CS(jtheta / 30 * math.tau / 4) for jtheta in range(31)]
	rs, zs = zip(*[(1.6 * s, 24 * c) for c, s in CSs])
	for face in island(rs, zs, [], 20):
		for vertex in face:
			f = 0.5 + 0.4 * noiseat(world.perp(vertex, world.zhat), [1, 0.7, 0.5])
			glColor3fv(math.mix([0.4, 0.4, 0.4], [0.6, 0.6, 0.6], f))
			x, y, z = vertex
			d = (24 - z) * (6 + z) / 24 ** 2 * 6
			C, S = math.CS(0.5 * z)
			glVertex3fv(world.plus(vertex, [C * d, S * d, 0]))
	glEnd()
	glEndList()

	lists.trunk = glGenLists(1)
	glNewList(lists.trunk, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	CSs = [math.CS(jtheta / 8 * math.tau / 4) for jtheta in range(9)]
	rs, zs = zip(*[(2 * s, 24 * c) for c, s in CSs])
	for face in island(rs, zs, [], 7):
		f = 0.8 + 0.2 * math.dot(world.normal(face), math.norm([1, 1, 1]))
		glColor3fv(world.times((0.6, 0.4, 0.2), f))
		for x, y, z in face:
			x += 0.03 * z * (z - 20)
			glVertex3f(x, y, z)
	glEnd()
	glEndList()

	lists.leaf0 = glGenLists(1)
	glNewList(lists.leaf0, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	rs, zs = [], []
	for jz in range(13):
		z = -jz
		r = 0.06 * z * (12 + z)
		rs.append(r)
		zs.append(z)
	for d in [-2, -1, 0, 1]:
		C0, S0 = math.CS(d * 0.6)
		C1, S1 = math.CS((d + 1) * 0.6)
		for j in range(12):
			v0 = rs[j] * C0, rs[j] * S0, zs[j]
			v1 = rs[j] * C1, rs[j] * S1, zs[j]
			v2 = rs[j+1] * C0, rs[j+1] * S0, zs[j+1]
			v3 = rs[j+1] * C1, rs[j+1] * S1, zs[j+1]
			for vertex in (v0, v2, v1, v1, v2, v3):
				glVertex3fv(vertex)
	glEnd()
	glEndList()


	lists.leaf = glGenLists(1)
	glNewList(lists.leaf, GL_COMPILE)
	glCullFace(GL_FRONT)
	glColor3f(0.0, 0.15, 0.0)
	glCallList(lists.leaf0)
	glCullFace(GL_BACK)
	glColor3f(0.1, 0.4, 0.1)
	glCallList(lists.leaf0)
	glEndList()

	lists.tree0 = glGenLists(1)
	glNewList(lists.tree0, GL_COMPILE)
	rendertree(0, force=True)
	glEndList()

	lists.tree1 = glGenLists(1)
	glNewList(lists.tree1, GL_COMPILE)
	rendertree(1, force=True)
	glEndList()

	lists.water = glGenLists(1)
	glNewList(lists.water, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	color0 = 0, 0.2, 0.4
	color1 = 0, 0.4, 0.4
	for face in sdata:
		for vertex in face:
			f = 0.5 + 0.3 * noiseat(vertex, [0.2, 0.07, 0.4])
			glColor3fv(math.mix(color0, color1, f))
			glVertex3fv(world.times(vertex, world.R))
	glEnd()
	glEndList()

	lists.backwater = glGenLists(1)
	glNewList(lists.backwater, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in sdata:
		for vertex in reversed(face):
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
			glVertex3fv(vertex)
	glEnd()
	glEndList()



	lists.seed = glGenLists(1)
	glNewList(lists.seed, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in world.usphere(3):
		for vertex in face:
			c = 0.3 + 0.05 * noiseat(vertex, [0.4, 0.3, 0.14], seed="seed")
			glColor4f(*world.times([1, 0.6, 0.4], c), 1)
			x, y, z = vertex
			glVertex3f(4 * x, 3 * y, 3 * z)
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

	lists.speck = glGenLists(1)
	glNewList(lists.speck, GL_COMPILE)
	glBegin(GL_TRIANGLES)
	for face in world.usphere(0):
		for vertex in face:
			glVertex3fv(world.times(vertex, 0.1))
	glEnd()
	glEndList()

	lists.splash = glGenLists(1)
	glNewList(lists.splash, GL_COMPILE)
	for a in range(30):
		glColor3fv(math.mix([0.3, 0.3, 0.5], [0.9, 0.9, 1.0], random.random()))
		glPushMatrix()
		glTranslate(*world.times(world.randomunit(), random.random() ** 0.3))
		glBegin(GL_TRIANGLES)
		for face in world.usphere(1):
			for vertex in face:
				glVertex3fv(world.times(vertex, math.fadebetween(a, 0, 0.03, 30, 0.05)))
		glEnd()
		glPopMatrix()
	glEndList()

	lists.discs = {}
	for color, (r, g, b) in settings.colors.items():
		CSs = [(C, S, 0) for C, S in math.CSround(60)]
		CSs = [(j, CSs[j], CSs[(j+1)%60]) for j in range(60)]
		lists.discs[color] = [glGenLists(1) for _ in range(4)]

		glNewList(lists.discs[color][0], GL_COMPILE)
		glColor3f(r, g, b)
		glBegin(GL_TRIANGLES)
		for j, p0, p1 in CSs:
			v0 = 0, 0, 0
			v1 = world.times(p0, 5)
			v2 = world.times(p1, 5)
			for vertex in (v0, v1, v2):
				glVertex3fv(vertex)
		glEnd()
		glEndList()

		glNewList(lists.discs[color][1], GL_COMPILE)
		glColor3f(r, g, b)
		glBegin(GL_TRIANGLES)
		for j, p0, p1 in CSs:
			if j % 30 < 3:
				continue
			v0 = world.times(p1, 11)
			v1 = world.times(p0, 11)
			v2 = world.times(p1, 7)
			v3 = world.times(p0, 7)
			for vertex in (v0, v2, v1, v1, v2, v3):
				glVertex3fv(vertex)
		glEnd()
		glEndList()

		glNewList(lists.discs[color][2], GL_COMPILE)
		glColor3f(r, g, b)
		glBegin(GL_TRIANGLES)
		for j, p0, p1 in CSs:
			if j % 20 < 2:
				continue
			v0 = world.times(p1, 14)
			v1 = world.times(p0, 14)
			v2 = world.times(p1, 12)
			v3 = world.times(p0, 12)
			for vertex in (v0, v2, v1, v1, v2, v3):
				glVertex3fv(vertex)
		glEnd()
		glEndList()

		glNewList(lists.discs[color][3], GL_COMPILE)
		glBegin(GL_TRIANGLES)
		for face in island([13, 13.1, 13.2, 13.3], [140, 90, 40, 5], [], 20):
			for vertex in face:
				x, y, z = vertex
				alpha = math.clamp((z - 5) * (130 - z) / 100 ** 2 * 0.8, 0, 1)
				glColor4f(r, g, b, alpha)
				glVertex3fv(vertex)
		glEnd()
		glEndList()

	
# Island height profile
isrs = [0, 2, 5, 10, 15, 20, 24, 25, 26, 30]
iszs = [6, 5.8, 5.5, 5, 3, 2, 1, 0, -2, -30]
def isr(z):
	if z > iszs[0]:
		return 0
	elif z < iszs[-1]:
		return isrs[-1]
	for j in range(len(isrs) - 1):
		if z >= iszs[j+1]:
			return math.fadebetween(z, iszs[j], isrs[j], iszs[j+1], isrs[j+1])
	return isrs[-1]

def renderisland(name, ispec, R):
	import time
	t0 = time.time()
	lists.islands[name] = glGenLists(1)
	glNewList(lists.islands[name], GL_COMPILE)
	glBegin(GL_TRIANGLES)
	rs = [r * R / 25 for r in isrs]
	for face in island(rs, iszs, ispec, 50):
		for vertex in face:
			x, y, z = vertex
			h = math.length([x, y, z + world.R]) - world.R
			h = h / 6 + 0.12 * noiseat(vertex, [10, 5, 2, 1])
			f = 0.8 + 0.2 * noiseat(vertex, [19, 13, 8], seed="shade")
			glColor3fv(world.times(acolor(h), f))
			glVertex3fv(vertex)
	glEnd()
	glEndList()

def rendertree(fbloom, force=False):
	if fbloom == 0 and not force:
		glCallList(lists.tree0)
	elif fbloom == 1 and not force:
		glCallList(lists.tree1)
	else:
		fbloom += 0.1
		glPushMatrix()
		glCallList(lists.trunk)
		glTranslatef(3, 0, 24)
		glRotate(32, 0, 1, 0)
		color0 = 0.1, 0.4, 0.1
		for j in range(20):
			fcolor = 0.8 + 0.2 * (math.phi ** 2 * j) % 1
			glPushMatrix()
			glRotate(360 * ((math.phi * j + (1 - fbloom) * j * 0.07) % 1), 0, 0, 1)
			glRotate(fbloom * math.mix(40, 140, j / 20), 0, 1, 0)
			glCullFace(GL_FRONT)
			glColor3fv(world.times(color0, fcolor * 0.5))
			glCallList(lists.leaf0)
			glCullFace(GL_BACK)
			glColor3fv(world.times(color0, fcolor))
			glCallList(lists.leaf0)
			glPopMatrix()
		glPopMatrix()


def drawstars():
	glDisable(GL_LIGHTING)
	glDisable(GL_TEXTURE_2D)
	glPushMatrix()
	view.perspectivestars()
	view.look()
	glScale(500, 500, 500)
	glCallList(lists.stars)
	glPopMatrix()

	glClear(GL_DEPTH_BUFFER_BIT)


def look():
	glPushMatrix()
	view.perspective()
	view.look()

def draw(youtoo = True):
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

	glPushMatrix()
	fwave = 1 + 0.001 * (0.5 * math.cycle(0.3 * 0.001 * pygame.time.get_ticks()) - 0.5)
	glScale(fwave, fwave, fwave)
	glTranslate(*world.times(state.rmoon, state.tide))
	f, l, u = world.wspot
	glMultMatrixf([*f,0,  *l,0,  *u,0,  0,0,0,1])
	glColor3fv(world.times(state.color0, 0.5))
	glCallList(lists.backwater)
	glPopMatrix()

	# Draw objects that can be seen underwater
	for effect in state.effects:
		if hasattr(effect, "udraw"):
			glPushMatrix()
			effect.orient()
			effect.udraw()
			glPopMatrix()


	glEnable(GL_BLEND)
	glBlendColor(0, 0, 0, 0.85)
	glBlendFunc(GL_CONSTANT_ALPHA, GL_ONE_MINUS_CONSTANT_ALPHA)

	glPushMatrix()
	glScale(fwave, fwave, fwave)
	glTranslate(*world.times(state.rmoon, state.tide))
	f, l, u = world.wspot
	glMultMatrixf([*f,0,  *l,0,  *u,0,  0,0,0,1])
	glCallList(lists.water)
	glPopMatrix()
	glDisable(GL_BLEND)


	for island in state.islands:
		glPushMatrix()
		island.orient()
		island.draw()
		glPopMatrix()

#	glPushMatrix()
#	glTranslate(0, 0, world.R)
#	glCallList(lists.island)
#	glPopMatrix()


	if state.moonrod is not None:
		glPushMatrix()
		state.moonrod.orient()
		glPushMatrix()
		state.moonrod.drawmoon()
		glPopMatrix()
		glCallList(lists.moonrod)
		glRotatef(120, 0, 0, 1)
		glCallList(lists.moonrod)
		glRotatef(120, 0, 0, 1)
		glCallList(lists.moonrod)
		glPopMatrix()


	if youtoo:
		glPushMatrix()
		state.you.orient()
	#	color = [0.8, 0.4, 0.0] if state.islands[-1].distout(state.you.up) > 0 else [0.8, 0.8, 0.8]
	#	glColor3fv(color)
		glColor3f(0.8, 0.4, 0.0)
		glCallList(lists.you)
		if False:
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
	
	for effect in state.effects:
		glPushMatrix()
		effect.orient()
		effect.draw()
		glPopMatrix()

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	for effect in state.effects:
		if hasattr(effect, "pdraw"):
			glPushMatrix()
			effect.orient()
			effect.pdraw()
			glPopMatrix()
	glDisable(GL_BLEND)
	

	if view.moonalpha() > 0:
		glEnable(GL_BLEND)
		glBlendColor(1, 0, 0, view.moonalpha())
		glBlendFunc(GL_CONSTANT_ALPHA, GL_ONE_MINUS_CONSTANT_ALPHA)
		glPushMatrix()
		glTranslate(*world.times(state.rmoon, 1.5 * world.R + state.dmoon))
		glScalef(*world.times([1, 1, 1], 0.5 * world.R))
		glCallList(lists.moon)
		glPopMatrix()
		glDisable(GL_BLEND)

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	for effect in state.effects:
		if hasattr(effect, "adraw"):
			glPushMatrix()
			effect.orient()
			effect.adraw()
			glPopMatrix()
	glDisable(GL_BLEND)

	glPopMatrix()


