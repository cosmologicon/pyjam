import pygame

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
qsavefile = None

keys = {
	"quit": [pygame.K_ESCAPE, pygame.K_q],
	"up": [pygame.K_UP],
	"right": [pygame.K_RIGHT],
	"left": [pygame.K_LEFT],
	"down": [pygame.K_DOWN],
	"swap": [pygame.K_TAB],
	"act": [pygame.K_SPACE],
	"hint": [pygame.K_LCTRL, pygame.K_RCTRL],
	
	"skip": [pygame.K_F1],

	"fullscreen": [pygame.K_F10],
	"resolution": [pygame.K_F11],
#	"step": [pygame.K_F2],
}


