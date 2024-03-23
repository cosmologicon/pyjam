import pygame, math
from . import view, pview, maff, grid

scale = 400
w0 = int(round(scale / 20))
kscale = 2

def minus(p0, p1):
	x0, y0, z0 = p0
	x1, y1, z1 = p1
	return x1 - x0, y1 - y0, z1 - z0

def cross(p0, p1):
	x0, y0, z0 = p0
	x1, y1, z1 = p1
	return y0 * z1 - z0 * y1, z0 * x1 - x0 * z1, x0 * y1 - y0 * x1

def trinormal(pGs):
	pG0, pG1, pG2 = pGs
	return math.norm(cross(minus(pG2, pG1), minus(pG1, pG0)))

light = math.norm((-1, 1, 1))

def lightnorm(normG):
	a = math.dot(normG, light)
	return math.interp(a, -1, 0.2, 1, 1)

def trilight(pGs):
	return lightnorm(trinormal(pGs))

def setcamera():
	global camera
	camx, camy, camz = 0, 0, 1
	camy, camz = math.R(view.tip, (camy, camz))
	camx, camy = math.R(-view.tilt, (camx, camy))
	camera = camx, camy, camz

def cullnorm(normG):
	return math.dot(normG, camera) > 0
def culltri(pGs):
	return cullnorm(trinormal(pGs))

def rendertri(surf, pGs, color0):
	if not culltri(pGs): return
	pDs = [view.DconvertG(pG[:2], pG[2]) for pG in pGs]
	color = math.mix((0, 0, 0), color0, trilight(pGs))
	pygame.draw.polygon(surf, color, pDs)
	

# Zig-zag pattern, e.g. top left, top right, bottom left, bottom right	
def renderquad(surf, pGs, color0):
	p0, p1, p2, p3 = pGs
	rendertri(surf, (p1, p0, p2), color0)
	rendertri(surf, (p1, p2, p3), color0)

def renderpoint(surf, pG, normG, color0):
	if not cullnorm(normG): return
	pD = view.DconvertG(pG[:2], pG[2])
	color = math.mix((0, 0, 0), color0, lightnorm(normG))
	surf.set_at(pD, color)
	

Rdome = 0.6
Rphi0 = 0.1
rtube = 0.14
rframe = 0.04
wframe = 0.02

def pdome(ftheta, fphi):
	theta = math.mix(0, math.tau, ftheta)
	phi = math.mix(Rphi0, math.tau / 4, fphi)
	x, y, z = Rdome, 0, 0
	x, z = math.R(phi, (x, z))
	x, y = math.R(theta, (x, y))
	z += math.cos(Rphi0) - 1
	return x, y, z


def renderdome(scale):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	ntheta = 10
	nphi = 3
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for jtheta in range(ntheta):
		for jphi in range(nphi):
			ps = [(theta, phi) for phi in (jphi, jphi + 1) for theta in (jtheta, jtheta + 1)]
			pGs = [pdome(theta / ntheta, phi / nphi) for theta, phi in ps]
			renderquad(surf, pGs, (255, 255, 255))
	return surf


def rendercity(scale):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	dome = renderdome(scale)
	dimg = dome.copy()
	dimg.fill((0, 0, 255, 60))
	dimg.blit(dome, (0, 0), None, pygame.BLEND_RGBA_MULT)
	img = dome.copy()
	buildings = []
	for j in range(200):
#		x = math.fuzzrange(-1, 1, 1200, j)
#		y = math.fuzzrange(-1, 1, 1201, j)
#		if math.hypot(x, y) > 1: continue
#		x *= 0.65
#		y *= 0.65
		r = math.fuzzrange(0, 0.48, 1204, j)
		theta = math.fuzzrange(0, math.tau, 1205, j)
		x, y = math.CS(theta, r)
		h = math.fuzzrange(0.05, 0.1, 1202, j)
		rect = pygame.Rect(0, 0, int(view.VscaleG * h), int(view.VscaleG * h))
		rect.midbottom = view.DconvertG((x, y))
		r = int(math.fuzzrange(40, 80, 1203, j))
		g = int(math.fuzzrange(20, 40, 1204, j))
		b = int(math.fuzzrange(0, 20, 1205, j))
		buildings.append((rect.bottom, rect, (r, g, b)))
	buildings.sort()
	for _, rect, color in buildings:
		img.fill(color, rect)
	img.blit(dimg, (0, 0))
	return img
	


def pstraight(ftheta, a, beta):
	theta = math.tau * ftheta
	x, y, z = rtube, 2/3 * grid.s * 1.002 * math.mix(-1, 1, a), 0
	x, z = math.R(-theta, (x, z))
	z += rtube
	x, y = math.R(-beta, (x, y))
	return x, y, z

def pnormstraight(ftheta, a, beta):
	theta = math.tau * ftheta
	x, y, z = rtube, 2/3 * grid.s * 1.002 * math.mix(-1, 1, a), 0
	nx, ny, nz = 1, 0, 0
	x, z = math.R(-theta, (x, z))
	nx, nz = math.R(-theta, (nx, nz))
	z += rtube
	x, y = math.R(-beta, (x, y))
	nx, ny = math.R(-beta, (nx, ny))
	return (x, y, z), (nx, ny, nz)

# d = -1 left turn, d = 1 right turn
def pturn(ftheta, fphi, beta, d):
	theta = math.tau * ftheta
	phi = math.tau / 6 * (fphi * 1.004 - 0.002)
	x, y, z = -d + rtube * math.cos(theta), 0, rtube * math.sin(theta)
	x, y = math.R(-d * phi, (x, y))
	x += d
	y -= 2/3 * grid.s
	z += rtube
	x, y = math.R(-beta, (x, y))
	return x, y, z

def pnormturn(ftheta, fphi, beta, d):
	theta = math.tau * ftheta
	phi = math.tau / 6 * (fphi * 1.004 - 0.002)
	x, y, z = -d + rtube * math.cos(theta), 0, rtube * math.sin(theta)
	nx, ny, nz = math.cos(theta), 0, math.sin(theta)
	x, y = math.R(-d * phi, (x, y))
	nx, ny = math.R(-d * phi, (nx, ny))
	x += d
	y -= 2/3 * grid.s
	z += rtube
	x, y = math.R(-beta, (x, y))
	nx, ny = math.R(-beta, (nx, ny))
	return (x, y, z), (nx, ny, nz)


def parch(f):
	f = math.clamp(f, 0, 1)
	if 0 <= f < 0.1:
		return math.interp(f, 0, (-rtube - rframe, 0), 0.1, (-rtube - rframe, rtube))
	if 0.9 <= f <= 1:
		return  math.interp(f, 0.9, (rtube + rframe, rtube), 1, (rtube + rframe, 0))
	phi = math.interp(f, 0.1, math.tau / 4, 0.9, -math.tau / 4)
	x, y = math.R(phi, (0, rtube + rframe))
	y += rtube
	return x, y


def gamma(theta):
	theta += 0.25
	theta = (theta + 0.5) % 1 - 0.5
	return math.interp(abs(theta), 0, 1, 0.5, 0)

drawback = False

def renderstraight(scale, beta):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	ntheta = 60
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	if drawback:
		for jtheta in range(ntheta):
			ps = [(theta, a) for a in (1, 0) for theta in (jtheta, jtheta + 1)]
			pGs = [pstraight(theta / ntheta, a, beta) for theta, a in ps]
			renderquad(surf, pGs, (50, 50, 50))
	for dstripe in range(-10, 2, 1):
		color = (255, 255, 255)
		if dstripe % 2:
			color = math.imix(color, (0, 0, 0), 0.2)
		gs = {
			jtheta: math.clamp(0.5 * gamma(jtheta / ntheta) - dstripe / 4, 0, 1)
			for jtheta in range(ntheta + 1)
		}
		for jtheta in range(ntheta):
			ps = [(theta, a) for theta in (jtheta, jtheta + 1) for a in (gs[theta], 0)]
			pGs = [pstraight(theta / ntheta, a, beta) for theta, a in ps]
			renderquad(surf, pGs, color)
	return surf

def renderstraight(scale, beta, amax = 1, drawback = False):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill((255, 255, 255, 0))
	ntheta = kscale * scale
	na = kscale * scale
	if drawback:
		for jtheta in range(ntheta):
			ftheta = jtheta / ntheta
			for ja in range(na + 1):
				a = ja / na
				if a > amax: continue
				color = (50, 50, 50)
				pG, (nx, ny, nz) = pnormstraight(ftheta, a, beta)
				renderpoint(surf, pG, (-nx, -ny, -nz), color)
	for jtheta in range(ntheta):
		ftheta = jtheta / ntheta
		for ja in range(na + 1):
			a = ja / na
			if a > amax: continue
			color = (255, 255, 255)
			jstripe = gamma(ftheta) - 2 * a
			if jstripe % 1 < 0.5:
				color = math.imix((0, 0, 0), color, 0.7)
			pG, normG = pnormstraight(ftheta, a, beta)
			renderpoint(surf, pG, normG, color)
	return surf


def renderturn(scale, beta, d):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	ntheta = 400
	nphi = 160
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	if drawback:
		for jtheta in range(ntheta):
			for jphi in range(nphi):
				ps = [(theta, phi) for phi in (jphi, jphi + 1) for theta in (jtheta, jtheta + 1)]
				pGs = [pturn(theta / ntheta, phi / nphi, beta, d) for theta, phi in ps]
				renderquad(surf, pGs, (50, 50, 50))
	for dstripe in range(6, -2, -1):
		color = (255, 255, 255)
		if dstripe % 2:
			color = math.imix(color, (0, 0, 0), 0.2)
		gs = {
			jtheta: math.clamp(-0.5 * gamma(jtheta / ntheta) + dstripe / 4, 0, 1)
			for jtheta in range(ntheta + 1)
		}
		for jtheta in range(ntheta):
			for jphi in range(nphi):
				if gs[jtheta] < jphi / nphi:
					continue
				ps = [(theta, phi) for phi in (jphi + 1, jphi) for theta in (jtheta, jtheta + 1)]
				pGs = [pturn(theta / ntheta, phi / nphi, beta, d) for theta, phi in ps]
				renderquad(surf, pGs, color)
	return surf

def renderturn(scale, beta, d):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	ntheta = kscale * scale
	nphi = kscale * scale
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill((255, 255, 255, 0))
	for jtheta in range(ntheta):
		ftheta = jtheta / ntheta
		for jphi in range(nphi + 1):
			fphi = jphi / nphi
			color = (255, 255, 255)
			jstripe = gamma(ftheta) + 2 * fphi + 0.5
			if jstripe % 1 < 0.5:
				color = math.imix((0, 0, 0), color, 0.7)
			pG, normG = pnormturn(ftheta, fphi, beta, d)
			renderpoint(surf, pG, normG, color)
	return surf


def pdock(farch, a, beta):
	x, z = parch(farch)
	y = 2/3 * grid.s - math.sqrt(Rdome ** 2 - x ** 2 - (z + Rphi0) ** 2)
	y *= -a
	x, y = math.R(-beta, (x, y))
	return x, y, z

def renderdock(scale, beta):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	narch = 100
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for jarch in range(narch + 1):
		farch0 = jarch / narch
		farch1 = (jarch + 1) / narch
		ps = [(farch, a) for farch in (farch0, farch1) for a in (0, 1)]
		pGs = [pdock(farch, a, beta) for farch, a in ps]
		renderquad(surf, pGs, (255, 255, 255))
		pGs = [(0, 0, 0), pdock(farch1, 0, beta), pdock(farch0, 0, beta)]
		rendertri(surf, pGs, (255, 255, 255))
	return surf


def prock(pG0, r, h, n, *seed):
	jtheta0 = math.fuzz(8000, *seed)
	pbase = [
		(x + math.fuzzrange(-1, 1, 8001, j, *seed) * 0.2 * r,
		y + math.fuzzrange(-1, 1, 8002, j, *seed) * 0.2 * r,
		0)
		for j, (x, y) in enumerate(math.CSround(n, r = r, jtheta0 = jtheta0, center = pG0))
	]
	ptop = [
		(x + math.fuzzrange(-1, 1, 8003, j, *seed) * 0.2 * r,
		y + math.fuzzrange(-1, 1, 8004, j, *seed) * 0.2 * r,
		0.7 * h + math.fuzzrange(-1, 1, 8005, j, *seed) * 0.2 * h)
		for j, (x, y) in enumerate(math.CSround(n, r = 0.8 * r, jtheta0 = jtheta0, center = pG0))
	]
	ptip = pG0[0], pG0[1], h
	for j in range(n):
		k = (j + 1) % n
		yield pbase[j], pbase[k], ptop[j], ptop[k]
#		yield pbase[j], ptop[k], ptop[j], ptop[j]
		yield ptop[j], ptop[k], ptip, ptip
	

rockcolor0 = 60, 40, 20
drockcolor = 10, 10, 10
def rockcolor(*seed):
	return [int(c0 + math.fuzzrange(-dc, dc, 9000, j, *seed))
		for j, (c0, dc) in enumerate(zip(rockcolor0, drockcolor))]

def renderrock(scale, *seed):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	ntheta = 10
	nphi = 3
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill(rockcolor0 + (0,))
	rockps = []
	for j in range(1000):
		x = math.fuzzrange(-1, 1, 6000, j, *seed)
		y = math.fuzzrange(-1, 1, 6001, j, *seed)
		if math.hypot(x, y) > 1: continue
		r = math.fuzzrange(0.12, 0.25, 6002, j, *seed)
		h = math.fuzzrange(1, 2.5, 6003, j, *seed) * r
		x *= 2/3 * grid.s - r + 0.1
		y *= 2/3 * grid.s - r + 0.1
		if any(math.hypot(x - x1, y - y1) < 0.8 * (r + r1) for x1, y1, r1, _, _ in rockps):
			continue
		color = rockcolor(j, *seed)
		rockps.append((x, y, r, h, color))
		n = int(math.fuzzrange(3, 6, 6004, j, *seed))
		if len(rockps) >= 10:
			break
	rockps.sort(key = lambda rockp: rockp[1], reverse = True)
	for j, (x, y, r, h, color) in enumerate(rockps):
		for quad in prock((x, y), r, h, 5, j, *seed):
			renderquad(surf, quad, color)
	return surf



def shave(img0, fname):
	print("shave", fname)
	w0, h0 = img0.get_size()
	ps = [(x, y) for x in range(w0) for y in range(h0) if img0.get_at((x, y))[3]]
	xs, ys = zip(*ps)
	xs = set(xs)
	ys = set(ys)
	w = 2 * max(max(xs) - w0 // 2, w0 // 2 - min(xs))
	h = 2 * max(max(ys) - h0 // 2, h0 // 2 - min(ys))
	img = pygame.Surface((w, h)).convert_alpha()
	img.fill((0, 0, 0, 0))
	img.blit(img0, (w // 2 - w0 // 2, h // 2 - h0 // 2))
	pygame.image.save(img, f"img/{fname}.png")


def glowify(img, w = w0):
	offsets = set((round(x), round(y)) for x, y in math.CSround(int(math.tau * w * 2), w))
	glowimg = img.copy()
	glowimg.fill((255, 255, 255, 0))
	for offset in offsets:
		glowimg.blit(img, offset, None, pygame.BLEND_RGBA_MAX)
	return glowimg

def glowshave(img0, fname):
	shave(img0, fname)
	shave(glowify(img0), f"{fname}-outline")


if __name__ == "__main__":
	pygame.init()
	pview.set_mode((2 * scale, 2 * scale))
	setcamera()
	for j in range(10):
		shave(renderrock(scale, j), f"rock-{j}")
	if False:
		glowshave(renderdome(scale), "dome")
		for jbeta in range(6):
			beta = jbeta * math.tau / 6
			glowshave(renderstraight(scale, beta), f"tube-{jbeta}-{jbeta}")
			# The turns take 7 hours to render at full resolution.
			jbetaL = (jbeta - 1) % 6
			glowshave(renderturn(scale, beta, -1), f"tube-{jbeta}-{jbetaL}")
			jbetaR = (jbeta + 1) % 6
			glowshave(renderturn(scale, beta, 1), f"tube-{jbeta}-{jbetaR}")
			glowshave(renderdock(scale, beta), f"dock-{jbeta}")
			glowshave(renderstraight(scale, beta, amax = 0.4, drawback = True), f"build-{jbeta}")
	if True:
		while not any(event.type in (pygame.QUIT, pygame.KEYDOWN) for event in pygame.event.get()):
			pview.fill((60, 30, 0))
			view.tip = math.cycle(pygame.time.get_ticks() * 0.0002)
			view.tilt = pygame.time.get_ticks() * 0.0001
			setcamera()
			img = renderrock(scale, 123)
			pview.screen.blit(img, (0, 0))
			pygame.display.flip()



