import pygame, math
from . import view, pview, maff, grid

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

def trilight(pGs):
	a = math.dot(trinormal(pGs), light)
	return math.interp(a, -1, 0, 1, 1)

def setcamera():
	global camera
	camx, camy, camz = 0, 0, 1
	camy, camz = math.R(view.tip, (camy, camz))
	camx, camy = math.R(-view.tilt, (camx, camy))
	camera = camx, camy, camz

def cull(pGs):
	return math.dot(trinormal(pGs), camera) > 0

def rendertri(surf, pGs, color0):
	if not cull(pGs): return
	pDs = [view.DconvertG(pG[:2], pG[2]) for pG in pGs]
	alpha = math.interp(trilight(pGs), 0, 0.4, 1, 1)
	color = math.mix((0, 0, 0), color0, alpha)
	pygame.draw.polygon(surf, color, pDs)
	
	
def renderquad(surf, pGs, color0):
	p0, p1, p2, p3 = pGs
	rendertri(surf, (p1, p0, p2), color0)
	rendertri(surf, (p1, p2, p3), color0)

Rdome = 0.6
Rphi0 = 0.1
rtube = 0.14
rframe = 0.04
wframe = 0.02
archcolor = (100, 90, 80)

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
	ntheta = 12
	nphi = 4
	surf = pygame.Surface((2 * scale, 2 * scale)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for jtheta in range(ntheta):
		for jphi in range(nphi):
			ps = [(theta, phi) for phi in (jphi, jphi + 1) for theta in (jtheta, jtheta + 1)]
			pGs = [pdome(theta / ntheta, phi / nphi) for theta, phi in ps]
			renderquad(surf, pGs, (255, 255, 255))
	return surf

def pstraight(ftheta, a, beta):
	theta = math.tau * ftheta
	x, y, z = rtube, 2/3 * grid.s * 1.01 * math.mix(-1, 1, a), 0
	x, z = math.R(-theta, (x, z))
	z += rtube
	x, y = math.R(-beta, (x, y))
	return x, y, z
# d = -1 left turn, d = 1 right turn
def pturn(ftheta, fphi, beta, d):
	theta = math.tau * ftheta
	phi = math.tau / 6 * (fphi * 1.02 - 0.01)
	x, y, z = -d + rtube * math.cos(theta), 0, rtube * math.sin(theta)
	x, y = math.R(-d * phi, (x, y))
	x += d
	y -= 2/3 * grid.s
	z += rtube
	x, y = math.R(-beta, (x, y))
	return x, y, z

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

def renderturn(scale, beta, d):
	view.VscaleG = scale
	view.xG0, view.yG0 = 0, 0
	pview.center = scale, scale
	ntheta = 40
	nphi = 16
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
		renderquad(surf, pGs, archcolor)
		pGs = [(0, 0, 0), pdock(farch1, 0, beta), pdock(farch0, 0, beta)]
		rendertri(surf, pGs, archcolor)
	return surf

def shave(img0, fname):
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

if __name__ == "__main__":
	pygame.init()
	pview.set_mode((800, 800))
	setcamera()
	shave(renderdome(400), "dome")
	for jbeta in range(6):
		beta = jbeta * math.tau / 6
		shave(renderstraight(400, beta), f"tube-{jbeta}-{jbeta}")
		jbetaL = (jbeta - 1) % 6
		shave(renderturn(400, beta, -1), f"tube-{jbeta}-{jbetaL}")
		jbetaR = (jbeta + 1) % 6
		shave(renderturn(400, beta, 1), f"tube-{jbeta}-{jbetaR}")
		shave(renderdock(400, beta), f"dock-{jbeta}")
	if True:
		while not any(event.type in (pygame.QUIT, pygame.KEYDOWN) for event in pygame.event.get()):
			pview.fill((60, 30, 0))
			view.tip = math.cycle(pygame.time.get_ticks() * 0.0002)
			view.tilt = pygame.time.get_ticks() * 0.0001
			setcamera()
			img = renderdock(400, 0)
			pview.screen.blit(img, (0, 0))
			pygame.display.flip()



