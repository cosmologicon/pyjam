import pygame

gamename = "Ares Firma"

# Resolution of the map. Decrease to improve performance.
# Potential impact on gameplay should be minimal.
mapres = 10

minfps, maxfps = 5, 120


size0 = 1280, 720
heights = 360, 540, 720, 1080, 1400
fullscreen = False

soundvolume = 1.0

DEBUG = False

keys = {
	"quit": pygame.K_ESCAPE,
	"resolution": pygame.K_F10,
	"fullscreen": pygame.K_F11,
	"screenshot": pygame.K_F12,
	"swap": pygame.K_TAB,
	"laststage": pygame.K_F1,
	"nextstage": pygame.K_F2,
	"tool1": pygame.K_1,
	"tool2": pygame.K_2,
	"tool3": pygame.K_3,
	"tool4": pygame.K_4,
}

