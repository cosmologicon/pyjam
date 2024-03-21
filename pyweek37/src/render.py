import pygame, math
from . import view, pview, maff

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

Rdome = 0.4
Rphi0 = 0.3

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
		theta0 = math.tau * jtheta / ntheta
		theta1 = math.tau * ((jtheta + 1) % ntheta) / ntheta
		for jphi in range(nphi):
			phi0 = math.tau * jphi / nphi
			phi1 = math.tau * ((jphi + 1) % nphi) / nphi
			ps = [(theta, phi) for phi in (jphi, jphi + 1) for theta in (jtheta, jtheta + 1)]
			pGs = [pdome(theta / ntheta, phi / nphi) for theta, phi in ps]
			renderquad(surf, pGs, (255, 255, 255))
	return surf


if __name__ == "__main__":
	pygame.init()
	pview.set_mode((800, 800))
	setcamera()
	pygame.image.save(renderdome(400), "img/dome.png")
	while not any(event.type == pygame.QUIT for event in pygame.event.get()):
		pview.fill((0, 0, 0))
		view.tip = math.cycle(pygame.time.get_ticks() * 0.0002)
		view.tilt = pygame.time.get_ticks() * 0.0001
		setcamera()
		img = renderdome(400)
		pview.screen.blit(img, (0, 0))
		pygame.display.flip()



