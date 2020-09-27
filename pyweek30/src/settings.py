import pygame, sys

gamename = "The Tide Summoner"

size0 = 1280, 720
height = 720
heights = 360, 540, 720, 960, 1200
fullscreen = False
forceres = False

minfps, maxfps = 5, 120

musicvolume = 1

easymode = False

qsavefile = "savegame-auto.pkl"
qsavetime = 5
reset = False

for arg in sys.argv:
	if arg.startswith("--res="):
		height = int(arg[6:])
if "--fullscreen" in sys.argv:
	fullscreen = True
if "--forceres" in sys.argv:
	forceres = True
if "--easymode" in sys.argv:
	easymode = True
if "--reset" in sys.argv:
	reset = True

colors = {
	"white": [0.8, 0.8, 0.8],
	"black": [0, 0, 0],
	"red": [1, 0.5, 0.5],
	"blue": [0.6, 0.6, 1],
	"yellow": [1, 1, 0.4],
}


keys = {
	"quit": [pygame.K_ESCAPE, pygame.K_q],
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"left": [pygame.K_LEFT, pygame.K_a],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"swap": [pygame.K_TAB],
	"act": [pygame.K_SPACE, pygame.K_RETURN],
	"hint": [pygame.K_LCTRL, pygame.K_RCTRL],
	
	"skip": [pygame.K_F1],

	"resolution": [pygame.K_F10],
	"fullscreen": [pygame.K_F11],
#	"step": [pygame.K_F2],
}


