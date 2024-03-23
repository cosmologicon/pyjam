import pygame, pickle, os.path

gamename = "Planet Hardscrabble"
savefile = "save-{mode}.pkl"
settingsfile = "settings.pkl"
autosave_seconds = 5

minfps, maxfps = 10, 120

sfxvolume = 0.6
musicvolume = 0.6

DEBUG = True

keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"act": [pygame.K_SPACE, pygame.K_RETURN],
	"remove": [pygame.K_BACKSPACE, pygame.K_DELETE],
	"resolution": [pygame.K_F10],
	"fullscreen": [pygame.K_F11],
	"screenshot": [pygame.K_F12],
	"quit": [pygame.K_ESCAPE],
	"zoomin": [pygame.K_1],
	"zoomout": [pygame.K_2],
}

size0 = 1280, 720
height = None
fullscreen = False
forceres = False

heights = 360, 480, 540, 720, 1080

# Can be any of the below palettes. Set to None to trigger the color selection screen.
palette = None
colors = "ROYGB"

PALETTES = {
	"roygb": {
		"R": [255, 50, 50],
		"O": [255, 128, 0],
		"Y": [255, 255, 0],
		"G": [50, 255, 50],
		"B": [100, 100, 255],
	},
	"roybw": {
		"R": [255, 50, 50],
		"O": [255, 128, 0],
		"Y": [255, 255, 0],
		"G": [100, 100, 255],
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
Xcolor = [100, 0, 0]

def resolvepalette(palette_):
	return palette_ or palette
def getcolor(colorname, palette = None):
	if colorname == "X": return Xcolor
	return PALETTES[resolvepalette(palette)].get(colorname, (40, 40, 40))



# Can be "off", "dim", or "on".
showdemand = "dim"
showsupply = "dim"

expandinfo = True

minzoom, maxzoom = 32, 160
# Evenly log-spaced.
zooms = [round(minzoom * (maxzoom / minzoom) ** (j/20), 2) for j in range(21)]

def save():
	obj = height, fullscreen, forceres, palette, showdemand, showsupply, expandinfo
	pickle.dump(obj, open(settingsfile, "wb"))

# Do I actually need this to be a function?
def load():
	global height, fullscreen, forceres, palette, showdemand, showsupply, expandinfo
	if not os.path.exists(settingsfile):
		return
	obj = pickle.load(open(settingsfile, "rb"))
	height, fullscreen, forceres, palette, showdemand, showsupply, expandinfo = obj
load()


