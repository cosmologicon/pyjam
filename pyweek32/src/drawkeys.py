import pygame, math
from functools import lru_cache
from . import maff, pview, ptext


R0 = 100
Z = 2
R = R0 * Z
size = w, h = 2 * R, 2 * R

tsize = 100

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "righteous"

pygame.display.init()
pview.set_mode(size)


last_update = 0
def display(img, force = False):
	global last_update
	if pygame.time.get_ticks() - last_update < 100 and not force:
		return
	last_update = pygame.time.get_ticks()
	pview.fill((20, 20, 40))
	pview.screen.blit(img, (0, 0))
	pygame.display.flip()

coords = []
for py in range(h):
	y = -(py - R + 0.5) / (R - 0.5)
	for px in range(w):
		x = (px - R + 0.5) / (R - 0.5)
		z2 = 1 - (x ** 2 + y ** 2)
		z = None if z2 < 0 else math.sqrt(z2)
		coords.append(((px, py), (x, y, z)))


@lru_cache(None)
def charimage(c):
	 img = pygame.Surface((tsize, tsize)).convert_alpha()
	 img.fill((0, 0, 0, 0))
	 ptext.draw(c, center = img.get_rect().center, fontsize = int(1.2 * tsize), surf = img)
	 return img

def samplechar(c, tx, ty):
	img = charimage(c)
	w, h = img.get_size()
	p = math.imix(0, w - 1, tx), math.imix(h - 1, 0, ty)
	return img.get_at(p).a / 255


def makeimg(color0, c, kappa, beta, gamma):
	img = pview.screen.copy().convert_alpha()
	img.fill(color0 + (0,))
	Rbeta = math.R(-beta)
	Rgamma = math.R(gamma)
	for j, (pixel, (x, y, z)) in enumerate(coords):
		transparent = z is None
			x, y = math.norm(x, y)
			z = 0
		dlight = math.fadebetween(math.dot((x, y, z), math.norm((0, 1, 1))), -0.2, 0.4, 1, 1)
		scolor0 = math.imix(color0, (0, 0, 0), 0.3)
		scolor1 = math.imix(color0, (0, 0, 0), 0.15)

		y, z = Rbeta((y, z))
		x, y = Rgamma((x, y))


		theta = math.atan2(x, z) % math.tau
		phi = math.atan2(y, math.hypot(x, z))
		color = color0
		if -0.5 < phi < 0.5:
			tx = (theta * 6 / math.tau + kappa) % 1
			ty = (phi * 1.1 + 0.5)
			color = math.imix(color0, (255, 255, 255), 0.3)
			if c:
				color = math.imix(color, (0, 0, 0), samplechar(c, tx, ty))
			if not 0.04 < tx < 0.96:
				color = scolor1
			

		sx = (theta * 12 / math.tau - 2 * kappa) % 1
		if 0.5 < abs(phi) < 0.62:
			color = scolor1
		if abs(phi) > 1.16:
			color = scolor1
		if 0.58 < abs(phi) < 1.4 and not 0.1 < sx < 0.9:
			color = scolor1

		if 0.5 < abs(phi) < 0.58:
			color = scolor0
		if abs(phi) > 1.2:
			color = scolor0
		if 0.5 < abs(phi) < 1.4 and not 0.05 < sx < 0.95:
			color = scolor0

		if transparent:
			color = color + (0,)
		img.set_at(pixel, math.imix((0, 0, 0), color, dlight))
		if j % 1000 == 0:
			display(img)
		
	display(img, force = True)
	return pygame.transform.smoothscale(img, (2 * R0, 2 * R0))

# fname, color0, char, winding, beta, gamma
settings = [
	("key", (30, 150, 180), "", False, 0.3, 0.15),
	("key2", (30, 150, 180), "2", False, 0.1, -0.15),
	("key3", (30, 150, 180), "3", False, 0.4, 0.05),
	("key4", (30, 150, 180), "4", False, -0.2, -0.05),
]


for fname, color0, char, winding, beta, gamma in settings:
	for j in range(60):
		kappa = j / 60 + 0.4
		if winding:
			gamma = math.tau * j / 60
		img = makeimg(color0, char, kappa, beta, gamma = gamma)
		pygame.image.save(img, "img/frames/%s-%d.png" % (fname, j))

def hasquit():
	for event in pygame.event.get():
		if event.type in (pygame.KEYDOWN, pygame.QUIT):
			return True
	return False

while not hasquit():
	pass


