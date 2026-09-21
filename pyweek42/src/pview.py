# view module - convenience methods for pygame.display - CC0
# https://github.com/cosmologicon/pygame-view

from __future__ import division
import pygame, math, os.path, datetime

WINDOW_FLAGS = 0
FULLSCREEN_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF
SCREENSHOT_DIRECTORY = "."
SCREENSHOT_TEMPLATE = "screenshot-%Y%m%d%H%M%S.png"

size0 = None
_height = None
_fullscreen = False
_forceres = False
_EMPTY_SENTINEL = ()
def set_mode(size0 = None, height = _EMPTY_SENTINEL, fullscreen = None, forceres = None):
	global _height, _fullscreen, _forceres
	if size0 is not None:
		_set_size0(size0)
	if height is not _EMPTY_SENTINEL:
		_height = int(round(height))
	if fullscreen is not None:
		_fullscreen = fullscreen
	if forceres is not None:
		_forceres = forceres
	_update()

def _set_size0(r):
	global size0
	w, h = r
	size0 = int(w), int(h)

def cycle_height(heights, reverse = False):
	heights = list(heights)
	if _height is None:
		height = max(heights) if reverse else min(heights)
	elif reverse:
		ok_heights = [height for height in heights if height < _height]
		height = max(ok_heights or heights)
	else:
		ok_heights = [height for height in heights if height > _height]
		height = min(ok_heights or heights)
	set_mode(height = height)

def toggle_fullscreen():
	set_mode(fullscreen = not _fullscreen)

def _update():
	if size0 is None:
		raise ValueError("view.size0 must be set")
	w0, h0 = size0
	if _forceres or not _fullscreen:
		w, h = size0 if _height is None else (int(round(w0 * _height / h0)), _height)
	else:
		w, h = _get_max_fullscreen_size(size0)
	flags = FULLSCREEN_FLAGS | pygame.FULLSCREEN if _fullscreen else WINDOW_FLAGS
	pygame.display.set_mode((w, h), flags)
	_setattrs()

def _get_max_fullscreen_size(size0):
	w0, h0 = size0
	modes = pygame.display.list_modes()
	if not modes:
		raise ValueError("No fullscreen display modes available.")
	# Being a little overly cautious here and not assuming that there's a single
	# aspect ratio that's at least as large as all the others in both dimensions.
	return max(
		min((w, int(round(w * h0 / w0))), (int(round(h * w0 / h0)), h))
		for w, h in modes
	)

def T(x, *args):
	if args:
		return [T(a) for a in (x,) + args]
	if isinstance(x, pygame.Rect):
		return pygame.Rect([T(a) for a in x])
	try:
		return [T(a) for a in x]
	except TypeError:
		return int((math.ceil if x > 0 else math.floor)(x * f))

def I(x, *args):
	if args:
		return [I(a) for a in (x,) + args]
	if isinstance(x, pygame.Rect):
		return pygame.Rect([I(a) for a in x])
	try:
		return [I(a) for a in x]
	except TypeError:
		return int((math.ceil if x > 0 else math.floor)(x))

def _setattrs():
	global screen, rect, rect0, aspect, diag, diag0, area, area0, s, s0, f
	rect0 = pygame.Rect((0, 0, size0[0], size0[1]))
	screen = pygame.display.get_surface()
	rect = screen.get_rect()
	rectattrs = ["x", "y", "top", "left", "bottom", "right",
		"topleft", "bottomleft", "topright", "bottomright",
		"midtop", "midleft", "midbottom", "midright",
		"center", "centerx", "centery", "size", "width", "height", "w", "h"]
	for attr in rectattrs:
		globals()[attr] = getattr(rect, attr)
		globals()[attr + "0"] = getattr(rect0, attr)
	diag = int(round(math.sqrt(w ** 2 + h ** 2)))
	diag0 = int(round(math.sqrt(w0 ** 2 + h0 ** 2)))
	area = w * h
	area0 = w0 * h0
	s = int(round(math.sqrt(area)))
	s0 = int(round(math.sqrt(area0)))
	aspect = w0 / h0
	f = h / h0

def fill(color, rect = None):
	# Color can be a color name string, a 3- or 4-tuple, or a pygame.Color object.
	try:
		color = pygame.Color(color)
	except ValueError:
		color = pygame.Color(*[min(max(int(round(a)), 0), 255) for a in color])
	rect = pygame.Rect(_resolverect(rect))
	if color.a == 255:
		screen.fill(color, rect)
	elif color.a == 0:
		return
	else:
		surf = pygame.Surface(rect.size).convert_alpha()
		surf.fill(color)
		screen.blit(surf, rect)

def _resolverect(r):
	return r or rect

def screenshot():
	if not os.path.exists(SCREENSHOT_DIRECTORY):
		os.makedirs(SCREENSHOT_DIRECTORY)
	fname = datetime.datetime.now().strftime(SCREENSHOT_TEMPLATE)
	pygame.image.save(screen, os.path.join(SCREENSHOT_DIRECTORY, fname))

