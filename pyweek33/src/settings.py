import pygame, sys

gamename = "On the Nature of Reflections"

minfps = 10
maxfps = 120
DEBUG = True
walkspeed = 1.6
showcontrols = False

keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"act": [pygame.K_SPACE, pygame.K_RETURN],
	"tip": [pygame.K_LSHIFT, pygame.K_RSHIFT],
	"next": [pygame.K_2],
	"prev": [pygame.K_1],
	"controls": [pygame.K_TAB],
	"zoomout": [pygame.K_LCTRL, pygame.K_RCTRL],
	"quit": [pygame.K_ESCAPE],
	"resolution": [pygame.K_F10],
	"fullscreen": [pygame.K_F11],
	"screenshot": [pygame.K_F12],
}
keys_by_code = { code: keyname for keyname, codes in keys.items() for code in codes }	

fullscreen = "--fullscreen" in sys.argv
forceres = "--forceres" in sys.argv
size0 = 1280, 720
heights = 480, 600, 720, 1080
height = 720
for arg in sys.argv:
	if arg.startswith("--res="):
		height = int(arg[6:])

