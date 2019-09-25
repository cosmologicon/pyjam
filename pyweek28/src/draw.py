# Draw world objects (i.e. in the middle panel)

from __future__ import division
import pygame, math, random, numpy
from . import pview, state, view
from .pview import T


# TODO(Christopher): Even though it's less realistic, I think it might look more dymanic if the
# starfield had a feeling of depth, i.e. not all the stars parallax the same amount when you move.
# my guess you fixed the A(angle?) for all the stars, so it should parallax the same amount?
# just add speed to A, and make it move to one direction, but it is not moving smooth, well, because the truncation int error?

def randomstar():
	z = random.uniform(0, 10000)
	A = random.uniform(0, 8)
	num = random.randint(50, 255)
	color = (num, num, num)
	return z, A, color
stardata = [randomstar() for _ in range(10000)]

def move_star(arg):
    z,A,color = arg
    speed = random.random()/1000
    return z,A+speed,color

# TODO: restrict to the central viewing area.
def stars():
    pview.fill((0, 0, 0))
    global stardata
    stardata = list(map(move_star,stardata))
    Nstar = 500  # TODO: change dynamically with resolution
    for z, A, color in stardata[:Nstar]:
        # TODO: dynamically change with camera zoom level
        pos = T(pview.centerx + 500 * view.dA(A, view.A), 300 * (z - view.zW0) % pview.h)
        # TODO: different colors correlated with depth
        pview.screen.set_at(pos, color)

def atmosphere():
    # Atmosphere
    alpha = pview.I(math.fadebetween(view.zW0, 10, 255, 100, 0))
    if alpha:
        pview.fill((100, 130, 220, alpha))



# Okay, here we go....

# The 3-D effect is achieved by constructing a numpy array to sample from a texture, which is a
# separately constructed pygame.Surface object.
# Every element in 3-D is an axially symmetric shape with a radius defined as a function with
# respect to height. We use an axis-aligned orthographic projection to determine the texture
# coordinates as a function of position within the image.
# Honestly, I'll need a whiteboard and an hour to explain most of these variables.
# See the notebook entry date 24 Sep 2019.
def getelement(tname, w, h, r0, r1, n, A0, k):
	texture = gettexture(tname)
	w0, h0 = texture.get_size()
	x = numpy.arange(w).reshape(w, 1)
	y = numpy.arange(h).reshape(1, h)
	b = 1 - (y + 1/2) / h
	r = getr(b, r0, r1, n)
	# TODO: optimize when r is a constant.
	a = (2 * x + 1 - w) / (2 * r)  # Broadcasting
	mask = abs(a) <= 1
	G = numpy.arcsin(a) * mask
	u = k * (G / math.tau - A0 / 8)
	v = 1 - b
	# Shading
	g = a + 0.2 * (a ** 2 - 1)
	f = 1 - abs(g ** 2)

	U = (u * w0 + 1/2).astype(int) % w0 * mask
	V = (v * h0 + 1/2).astype(int) % h0
	surf = pygame.Surface((w, h)).convert_alpha()
	arr0 = pygame.surfarray.pixels3d(texture)
	arr = pygame.surfarray.pixels3d(surf)
	arr[:, :, :] = (arr0[U, V, :] * f.reshape(w, h, 1)).astype(int)
#	arr[:, :, :] = arr0[U, V, :].astype(int)
	del arr
	pygame.surfarray.pixels_alpha(surf)[:,:] = 255 * mask
	return surf

_tcache = {}
def gettexture(tname):
	if tname in _tcache: return _tcache[tname]
	surf = pygame.Surface((100, 100)).convert()
	if tname == "window":
		surf.fill((100, 100, 100))
		surf.fill((100, 150, 255), pygame.Rect(10, 10, 80, 80))
	elif tname == "gray":
		surf.fill((120, 120, 120))
	else:
		raise ValueError
	_tcache[tname] = surf
	return surf

# r (radius of the element) with respect to b (vertical position).
# n is the ratio of the slope: n = dr(1)/db / dr(0)/db
# n = 1 is flat, n < 1 is concave, n > 1 is convex.
def getr(b, r0, r1, n):
	if n == 1: return r0 + (r1 - r0) * b
	D = (n * r0 - r1) / (n - 1)
	E = (r1 - r0) / (n - 1)
	F = math.log(n)
	return D + E * math.exp(F * b)

def drawelement(tname, xG, y0G, y1G, r0, r1, n, A0, k):
	x0, y0 = view.gametoview((xG, y0G))
	x0, y1 = view.gametoview((xG, y1G))
	r0 = view.zoom * r0
	r1 = view.zoom * r1
	w = int(math.ceil(2 * max(r0, r1)))
	h = y0 - y1
	surf = getelement(tname, w, h, r0, r1, n, A0, k)
	rect = surf.get_rect(midbottom = (x0, y0))
	if pview.rect.colliderect(rect):
		pview.screen.blit(surf, rect)



# TODO: when the camera is moving quickly (say, more than 100 pixels per frame), instead of drawing
# a textured cable, just do a solid color (with the shading). This will make it look more smeared
# out.
# Also the stars.

# Drawing the central cable
def buildcabletexture():
    global cabletexture
    w, h = 800, 400
    cabletexture = pygame.Surface((w, h)).convert()
    cabletexture.fill((80, 80, 80))
    for _ in range(100):
        # Stripe slope
        d = random.choice([1, 3, 5])
        n = random.randint(1, d // 2 + 1)
        flip = random.choice([False, True])
        n, d = (1, 3) if flip else (3, 5)
        xstep = pview.I(1 / d * w)
        dx = xstep * n
        # Stripe width
        s = random.randint(5, 10)
        color0 = random.randint(84, 90)
        color = [color0 + random.randint(-1, 1) for _ in range(3)]
        x0 = random.randint(0, w)
        y0, y1 = (0, h) if flip else (h, 0)
        while x0 + dx + s > 0:
            x0 -= xstep
        while x0 < w:
            ps = (x0, y0), (x0 + dx, y1), (x0 + dx + s, y1), (x0 + s, y0)
            pygame.draw.polygon(cabletexture, color, ps)
            x0 += xstep


cabletexture = None  # Will be built on the first call to getcablesurf


# The Surface used to tile the cable at a given zoom level and angle.
# TODO: caching. You don't want to cache every single surface generated by this function, but when
# the camera is stationary, this will be called with the same arguments frame after frame. A good
# compromise is just to cache the most recent call.
def getcablesurf(w, A):
    if cabletexture is None: buildcabletexture()
    w0, h0 = cabletexture.get_size()
    h = pview.I(w * h0 / w0 * math.pi)
    surf = pygame.Surface((w, h)).convert()

    # Range going from -1 to +1
    a = (numpy.arange(w) + 0.5) * 2 / w - 1
    # "Unwrapped" range of the angles covered by each column.
    b = numpy.arcsin(a) / math.tau - A / 8
    # Column within the image.
    xs = (b * w0 + 0.5).astype(int) % w0
    # Fade factor
    fs = 1 - abs(a ** 3)
    # Row within the image
    ys = ((numpy.arange(h) + 0.5) / h * h0 + 0.5).astype(int)

    arr0 = pygame.surfarray.pixels3d(cabletexture)
    arr = pygame.surfarray.pixels3d(surf)
    arr[:, :, :] = (arr0[xs.reshape(w, 1), ys.reshape(1, h), :] * fs.reshape(w, 1, 1)).astype(int)
    return surf

# Main entry point.
def cable():
    w = T(2 * state.radius * view.zoom)
    surf = getcablesurf(w, view.A)
    h = surf.get_height()
    hfull = T(state.top * view.zoom)
    # TODO: make this calculation more stable to small changes in view.zoom.
    xV, yV = view.gametoview((0, 0))
    # TODO: cut off at the top of the tower (or maybe just draw something over it so it looks like
    # the end.
    if yV - pview.h > h:
        yV = (yV - pview.h) % h + pview.h
    while yV > 0:
        rect = surf.get_rect(midbottom=(xV, yV))
        pview.screen.blit(surf, rect)
        yV -= h
