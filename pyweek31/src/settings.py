import sys, pickle, os
import pygame

gamename = "Gnorman's Copse"

# ADJUSTABLE IN-GAME

height = 720 # Resolution
fullscreen = False
forceres = False
soundvolume = 60
musicvolume = 60
mtrack = 0
showarrows = True
showmeter = True
nshade = 3
trails = True
speed = 1

def save():
	obj = height, fullscreen, forceres, soundvolume, musicvolume, mtrack, showarrows, showmeter, nshade, trails, speed
	pickle.dump(obj, open("settings.pkl", "wb"))

def load():
	global height, fullscreen, forceres, soundvolume, musicvolume, mtrack, showarrows, showmeter, nshade, trails, speed
	if os.path.exists("settings.pkl"):
		obj = pickle.load(open("settings.pkl", "rb"))
		height, fullscreen, forceres, soundvolume, musicvolume, mtrack, showarrows, showmeter, nshade, trails, speed = obj
if "--resetsettings" not in sys.argv:
	load()

size0 = 1280, 720  # Do not change.

# OKAY TO CHANGE HERE
savename = "progress.pkl"
qsavename = "quicksave.pkl"
tautosave = 5   # seconds
minfps = 10
maxfps = 120
vlevels = [0, 20, 40, 60, 80, 100]
heights = 360, 540, 720, 1080, 1440
speeds = [0.5, 1, 2, 5, 10]
tdrag = 0.3
ddrag = 15

keys = {
	"act": [pygame.K_SPACE],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"quit": [pygame.K_ESCAPE],
	"screenshot": [pygame.K_F12],
	"fullscreen": [pygame.K_F11],
	"resize": [pygame.K_F10],
}

# IBM color blind safe palette https://lospec.com/palette-list/ibm-color-blind-safe
colors = [
	(0x64, 0x8f, 0xff),
	(0xdc, 0x26, 0x7f),
	(0xff, 0xb0, 0x00),
]


# Command-line overrides.
reset = "--reset" in sys.argv
unlockall = "--unlockall" in sys.argv
DEBUG = "--DEBUG" in sys.argv
if "--fullscreen" in sys.argv:
	fullscreen = True
if "--forceres" in sys.argv:
	forceres = True
if "--noforceres" in sys.argv:
	forceres = False
if "--silence" in sys.argv:
	soundvolume = 0
	musicvolume = 0
if "--nofx" in sys.argv:
	nshade = 0
	trails = False
reset = "--reset" in sys.argv
for arg in sys.argv:
	if arg.startswith("--res="):
		height = int(arg[6:])




