import pygame

gamename = "Copse"

minfps = 10
maxfps = 120

fullscreen = False
forceres = False
heights = 360, 540, 720, 1080, 1440
size0 = w, h = width, height = 1280, 720

savename = "savegame.pkl"
tautosave = 15   # seconds

DEBUG = True

keys = {
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

