import pygame, pickle, os.path

gamename = "Space Age Tube"
savefile = "savefile.pkl"
settingsfile = "settings.pkl"


minfps, maxfps = 10, 120

keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"act": [pygame.K_SPACE, pygame.K_RETURN],
	"remove": [pygame.K_BACKSPACE, pygame.K_DELETE],
}

size0 = 1280, 720
height = None
fullscreen = False
forceres = False

# Can be any of the below palettes. Set to None to trigger the color selection screen.
palette = None
colors = "ROYGB"

PALETTES = {
	"roygb": {
		"R": [255, 50, 50],
		"O": [255, 150, 0],
		"Y": [222, 222, 0],
		"G": [50, 255, 50],
		"B": [80, 80, 255],
	},
	"roybw": {
		"R": [255, 50, 50],
		"O": [255, 150, 0],
		"Y": [222, 222, 0],
		"G": [80, 80, 255],
		"B": [200, 200, 200],
	},
	# https://lospec.com/palette-list/ibm-color-blind-safe
	"ibm": {
		"R": [0x64, 0x8f, 0xff],
		"O": [0x78, 0x5e, 0xf0],
		"Y": [0xdc, 0x26, 0x7f],
		"G": [0xfe, 0x61, 0x00],
		"B": [0xff, 0xb0, 0x00],
	},
}

def resolvepalette(palette_):
	return palette_ or palette
def getcolor(colorname, palette = None):
	return PALETTES[resolvepalette(palette)].get(colorname, (40, 40, 40))



# Can be "off", "dim", or "on".
showdemand = "dim"
showsupply = "dim"

def save():
	obj = height, fullscreen, forceres, palette, showdemand, showsupply
	pickle.dump(obj, open(settingsfile, "wb"))

# Do I actually need this to be a function?
def load():
	global height, fullscreen, forceres, palette, showdemand, showsupply
	if not os.path.exists(settingsfile):
		return
	obj = pickle.load(open(settingsfile, "rb"))
	height, fullscreen, forceres, palette, showdemand, showsupply = obj
load()


