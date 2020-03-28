import pygame, sys

gamename = "Miranda the Lepidopterist"
savename = "savegame.pkl"

# Resolution options
size0 = 1280, 720
height0 = 720
heights = 360, 540, 720, 1080
fullscreen = "--fullscreen" in sys.argv
forceres = "--forceres" in sys.argv

if "--tiny" in sys.argv:
	height0 = 360
if "--small" in sys.argv:
	height0 = 540
if "--large" in sys.argv:
	height0 = 1080
for arg in sys.argv:
	if arg.startswith("--res="):
		height0 = int(arg[6:])

minfps, maxfps = 10, 120

soundvolume = 0.6
musicvolume = 0.6

nosound = "--nosound" in sys.argv or "--noaudio" in sys.argv
nomusic = "--nomusic" in sys.argv or "--noaudio" in sys.argv
noaudio = nosound and nomusic

# color accessibility mode
colormode = "--colormode" in sys.argv

# visual effects
nobackground = "--nobackground" in sys.argv  # Wallpaper
noglow = "--noglow" in sys.argv  # white outline around sprites
noshadow = "--noshadow" in sys.argv  # color phased copies of you that lag behind

DEBUG = "--DEBUG" in sys.argv
forgive = False  # Whether you fail if you enter an incorrect combo
reset = "--reset" in sys.argv

keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"act": [pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_LCTRL, pygame.K_z, pygame.K_x, pygame.K_RETURN],
	"swap": [pygame.K_TAB],
	"quit": [pygame.K_ESCAPE],
	"forfeit": [pygame.K_q, pygame.K_BACKSPACE],
	"screenshot": [pygame.K_F12],
	"resolution": [pygame.K_F11],
	"fullscreen": [pygame.K_F10],

	# Cheat codes, only work in DEBUG mode
	"unlockall": [pygame.K_F1],
	"beatcurrent": [pygame.K_F2],
	# Editor
	"toggleguide": [pygame.K_1],
}

dtcombo = 0.2

