import sys
import pygame

gamename = "Gnorman's Copse"

minfps = 10
maxfps = 120

fullscreen = False
forceres = False
heights = 360, 540, 720, 1080, 1440
size0 = w, h = width, height = 1280, 720

savename = "savegame.pkl"
tautosave = 5   # seconds

soundvolume = 0.8
musicvolume = 0.8
mtrack = 0

speed = 1
speeds = [0.5, 1, 2, 5, 10]
reset = "--reset" in sys.argv
unlockall = "--unlockall" in sys.argv

DEBUG = "--DEBUG" in sys.argv

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


