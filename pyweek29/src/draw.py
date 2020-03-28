import pygame, numpy, math, scipy.ndimage
from functools import lru_cache
from . import pview, view, settings
from .pview import T

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

@lru_cache(None)
def getimg0(filename):
	return pygame.image.load("img/%s.png" % filename).convert_alpha()

@lru_cache(None)
def getbackground0(filename):
	return pygame.image.load("background/%s" % filename).convert_alpha()

def xform(img, scale, angle, hflip, vfactor, colormask, owidth, ocolor):
	if abs(vfactor) != 1:
		w, h = img.get_size()
		size = pview.I([w, h * abs(vfactor)])
		img = pygame.transform.smoothscale(img, size)
	vflip = vfactor < 0
	if hflip or vflip:
		img = pygame.transform.flip(img, hflip, vflip)
	if angle:
		img = pygame.transform.rotate(img, angle)
	if isinstance(scale, tuple):
		size = scale
	else:
		size = pview.I([a * scale / 2000 for a in img.get_size()])
	img = pygame.transform.smoothscale(img, size)
	if colormask is not None:
		colorarr = numpy.array(colormask).reshape([1, 1, 3]) / 256.0
		arr = pygame.surfarray.pixels3d(img)
		arr[:,:,:] = (arr * colorarr).astype(arr.dtype)
		del arr
	return outline(img, owidth, ocolor)


@lru_cache(1000)
def getimg(filename, scale, angle = 0, flip = False, vfactor = 1, colormask = None, owidth = 0, ocolor = (255, 255, 255)):
	return xform(getimg0(filename), scale, angle, flip, vfactor, colormask, owidth, ocolor)

@lru_cache(2)
def getbackground(filename, wmin, hmin):
	img = getbackground0(filename)
	w0, h0 = img.get_size()
	w, h = pview.I(max((wmin, wmin * h0 / w0), (hmin * w0 / h0, hmin)))
	return pygame.transform.smoothscale(img, (w, h))




specs = {
	"standing": ("backarm", "stand", "torso", "armdown"),
	"falling": ("backarm", "drop", "torso", "armup"),
	"leap0": ("backarm", "leap", "torso", "armout"),
	"leap1": ("backarm", "leap", "torso", "pointing"),
	"leap2": ("backarm", "leap", "torso", "elbowup"),
	"leap3": ("backarm", "leap", "torso", "armup"),
	"leap4": ("backarm", "leap", "torso", "armdown"),

	"pose-horiz-0": ("backarm", "leap", "torso", "pointing"),
	"pose-horiz-1": ("backarm", "leap", "torso", "elbowup"),
	"pose-horiz-2": ("backarm", "leap", "torso", "armout"),
	"pose-horiz-3": ("backarm", "leap", "torso", "armdown"),
	"pose-horiz-4": ("backarm", "bound", "torso", "pointing"),
	"pose-horiz-5": ("backarm", "bound", "torso", "elbowup"),
	"pose-horiz-6": ("backarm", "bound", "torso", "armout"),
	"pose-horiz-7": ("backarm", "bound", "torso", "armdown"),
}

@lru_cache(None)
def youimg0(spec):
	topimg = getimg0("you-%s" % spec[-1])
	if len(spec) == 1:
		return topimg.copy()
	else:
		img = youimg0(spec[:-1]).copy()
		img.blit(topimg, (0, 0))
		return img

#		img = pygame.Surface((2020, 2152)).convert_alpha()
#		img.fill((0, 0, 0, 0))
#		for filename in specs[spec]:
#			img.blit(getimg0("you-%s" % filename), (0, 0))


def colorshift(img, seed):
	img = img.copy()
	arr = pygame.surfarray.pixels3d(img)
	shift = numpy.array([[[1.234 * seed + 2, 1.345 * seed + 3, 1.456 * seed + 4]]]) * 256 % 256
	shifted = 127.0 + 127 * numpy.sin((math.tau / 256) * (arr + shift))
	arr[:,:,:] = shifted.astype(arr.dtype)
	return img

@lru_cache(None)
def youimg(spec, scale, angle, faceright, seed = None, owidth = None, ocolor = (255, 255, 255)):
	if seed is not None:
		return colorshift(youimg(spec, scale, angle, faceright), seed)
	return xform(youimg0(specs[spec]), 4 * scale, angle, not faceright, 1, None, owidth, ocolor)


def fade(img, alpha):
	if alpha == 1:
		return img
	img = img.copy()
	arr = pygame.surfarray.pixels_alpha(img)
	arr[:,:] = (arr * alpha).astype(arr.dtype)
	return img

def outline(img, width = 2, color = (255, 255, 255)):
	if not width:
		return img
	back = img.copy()
	r, g, b = color
	back.fill((r, g, b, 0))
	arr = pygame.surfarray.pixels_alpha(img)
	blur = scipy.ndimage.filters.gaussian_filter(arr, width)
	barr = pygame.surfarray.pixels_alpha(back)
	barr[:,:] = numpy.minimum(blur, 255 // 3) * 3
	del arr, barr
	back.blit(img, (0, 0))
	return back
	

def you(spec, screenpos, scale, angle, faceright, seed = None,
	alpha = None, owidth = None, ocolor = (255, 255, 255)):
	angle = int(round(angle)) % 360
	img = youimg(spec, scale, angle, faceright, seed, owidth, ocolor)
	if alpha is not None:
		img = fade(img, alpha)
	if screenpos is not None:
		rect = img.get_rect(center = screenpos)
		pview.screen.blit(img, rect)

def drawimg(filename, screenpos, scale, angle = 0, flip = False, vfactor = 1, colormask = None, owidth = 0, ocolor = (255, 255, 255)):
	angle = int(round(angle)) % 360
	vfactor = round(vfactor, 1)
	if vfactor == 0:
		return
	img = getimg(filename, scale, angle, flip, vfactor, colormask, owidth, ocolor)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)

@lru_cache(None)
def getlepimg(scale, angle, flip, vfactor, colormask):
	img0 = getimg("lep-body", scale, angle, flip)
	if vfactor != 0:
		img1 = getimg("lep-flap", scale, angle, flip, vfactor, colormask = colormask)
		img = img1.copy()
		img.fill((0, 0, 0, 0))
		img.blit(img0, img0.get_rect(center = img.get_rect().center))
		img.blit(img1, (0, 0))
	else:
		img = img0
	return outline(img)

def lep(screenpos, scale, angle, flip, vfactor, colormask):
	angle = int(round(angle)) % 360
	vfactor = round(vfactor, 1)
	img = getlepimg(scale, angle, flip, vfactor, colormask)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)
	


@lru_cache(None)
def getarrowimg0():
	img = pygame.Surface((240, 240)).convert_alpha()
	img.fill((0, 0, 0, 0))
	ps = (120, 20), (180, 70), (120, 220), (60, 70)
	pygame.draw.polygon(img, (0, 0, 0), ps)
	ps = (120, 30), (170, 70), (120, 200), (70, 70)
	pygame.draw.polygon(img, (255, 255, 255), ps)
	return img

@lru_cache(1000)
def getarrowimg(scale, d, color0, f, alpha, owidth):
	color = math.imix(color0, (255, 255, 255), 0.5)
	alpha = math.mix(alpha, 1, 0.5)
	img = getarrowimg0().copy()
	xs = numpy.arange(float(240)).reshape([240, 1, 1])
	ys = numpy.arange(float(240)).reshape([1, 240, 1])
	mask = ((-ys + 0.9 * abs(xs - 120)) * 0.006 - f) % 1 * 0.4 + 0.6
	colorarr = numpy.array(color).reshape([1, 1, 3]) / 256.0
#	arr = pygame.surfarray.pixels3d(img1)
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = (arr * mask * colorarr).astype(arr.dtype)
	del arr
#	img0.blit(img1, (0, 0))
	dx, dy = d
	img = pygame.transform.rotate(img, math.degrees(math.atan2(-dx, dy)))
	size = pview.I([a * scale / 240 for a in img.get_size()])
	img = pygame.transform.smoothscale(img, size)
	return fade(outline(img), alpha)

def arrow(screenpos, scale, d, color0, f, alpha, owidth = 2):
	f = int(f * 8) % 8 / 8
	img = getarrowimg(scale, d, color0, f, alpha, owidth)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)

@lru_cache(10)
def groundtexture0(colormask):
	x0, y0 = 100, 100
	img = pygame.Surface((x0, y0)).convert()
	colorarr = numpy.array(colormask).reshape([1, 1, 3]) / 256.0
	values = 1.0 - 0.15 * numpy.random.rand(x0, y0, 1) - 0.05 * numpy.random.rand(x0, y0, 3)
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = (255 * values * colorarr).astype(arr.dtype)
	return img

@lru_cache(1)
def groundtexture(w, h, offset, colormask):
	w0, h0 = w + 8, h + 8
	wi, hi = w0 // 8, h0 // 8
	img0 = groundtexture0(colormask)
	arr0 = pygame.surfarray.pixels3d(img0)
	xs = (numpy.arange(wi).reshape([wi, 1]) - wi / 2 + offset) / 8
	ys = numpy.arange(hi).reshape([1, hi]) / 2
	W = 1 / (0.5 + ys / 20)
	xs = (xs * W).astype(int) % 100
	ys = (ys * W).astype(int) % 100
	img = pygame.Surface((wi, hi)).convert()
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = arr0[xs,ys,:]
	return pygame.transform.smoothscale(img, (w0, h0))

@lru_cache(1)
def curtain(w, h, color):
	img = pygame.Surface((w, h)).convert_alpha()
	img.fill(color)
	factor = numpy.minimum(numpy.arange(h).reshape([1, h]) / h * 10.2, 1)
	arr = pygame.surfarray.pixels_alpha(img)
	arr[:,:] = (arr * factor).astype(arr.dtype)
	return img
	

def background(filename, gcolor):
#	pview.fill((200, 200, 200))
#	return
	(x0, y0), (wmin, hmin) = T(view.backgroundspec())
	img = getbackground(filename, wmin, hmin)
	pview.screen.blit(img, img.get_rect(midbottom = (x0, y0)))
	mtop = view.rrect.left // 2, y0 - T(40)
	if mtop[1] < pview.h:
		cimg = curtain(view.rrect.left, T(400), gcolor)
		pview.screen.blit(cimg, cimg.get_rect(midtop = mtop))
	return
	if y0 < pview.height:
		offset = T(view.zoom * view.cx)
		img = groundtexture(view.rrect.left, pview.height - y0, offset, (50, 80, 80))
		pview.screen.blit(img, img.get_rect(midtop = (x0, y0)))


def panel():
	img = getimg("paper", tuple(T(320, 720)))
	pview.screen.blit(img, img.get_rect(bottomright = pview.bottomright))

def loadimgs(scale):
	for f in set(f for filenames in specs.values() for f in filenames):
		getimg0("you-" + f)
		yield
	for spec in specs:
		for j in range(len(specs[spec])):
			youimg0(specs[spec][:j+1])
			yield
	for facingright in (True, False):
		for angle in (0, -28, -14, 14, 28):
			for pose0 in range(8):
				for j in (0, 1, 2):
					pose = (pose0 + 3 * j) % 8
					seed = 100 * pose + 17
					drawspec = "pose-horiz-%d" % pose
					if j == 0:
						you(drawspec, None, scale, angle, facingright)
					else:
						you(drawspec, None, scale, angle, facingright, seed, 1)
					yield
		you("standing", None, scale, 0, facingright)
		you("falling", None, scale, 0, facingright)




tokill = {}
def killtimeinit():
	global tokill
	youimg.cache_clear()
	tokill = { zoom: loadimgs(T(1.3 * zoom)) for zoom in view.allzooms }

def killtime(dt):
	z = view.zoom if view.zoom in tokill else pickany(tokill)
	if z is None:
		return
	tend = pygame.time.get_ticks() + dt * 1000
	while z in tokill and pygame.time.get_ticks() < tend:
		try:
			next(tokill[z])
		except StopIteration:
			del tokill[z]
			if settings.DEBUG:
				print("done", z, youimg.cache_info())
	if settings.DEBUG and pygame.time.get_ticks() - tend > 50:
		print("time:", pygame.time.get_ticks() - tend)

def finishkill():
	if view.zoom in tokill:
		for _ in tokill[view.zoom]:
			pass
		del tokill[view.zoom]

if __name__ == "__main__":
	from . import maff
	view.init()
	clock = pygame.time.Clock()
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		pview.fill((0, 0, 0))
		f = pygame.time.get_ticks() * 0.001 % 1
		arrow((500, 500), 240, (0, 1), (255, 255, 255), f, 1)
		pygame.display.flip()
	


