import pygame

gamename = "Ares Firma"

# Resolution of the map. Decrease to improve performance.
# Potential impact on gameplay should be minimal.
mapres = 10

minfps, maxfps = 5, 120


size0 = 1280, 720
heights = 480, 720, 1080
fullscreen = False

DEBUG = True

keys = {
	"quit": pygame.K_ESCAPE,
	"resolution": pygame.K_F10,
	"fullscreen": pygame.K_F11,
	"screenshot": pygame.K_F12,
	"swap": pygame.K_TAB,
	"laststage": pygame.K_F1,
	"nextstage": pygame.K_F2,
}

