import sys
import pygame

gamename = "Copse"

minfps = 10
maxfps = 120

fullscreen = False
forceres = False
heights = 360, 540, 720, 1080, 1440
size0 = w, h = width, height = 1280, 720

savename = "savegame.pkl"
tautosave = 5   # seconds

reset = "--reset" in sys.argv
unlockall = "--unlockall" in sys.argv

DEBUG = True

keys = {
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"quit": [pygame.K_ESCAPE],
	"screenshot": [pygame.K_F12],
	"fullscreen": [pygame.K_F11],
	"resize": [pygame.K_F10],
}

colors = [
	(100, 100, 255),
	(220, 220, 220),
	(200, 150, 50),
]

