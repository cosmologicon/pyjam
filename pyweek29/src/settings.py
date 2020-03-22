import pygame

gamename = "Butterfly Effect"

# Resolution options
size0 = 1280, 720
height0 = 720
heights = 360, 540, 720, 1080, 1440
fullscreen = False
forceres = False

minfps, maxfps = 10, 120

DEBUG = True

keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"act": [pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_LCTRL, pygame.K_z, pygame.K_x, pygame.K_RETURN],
	"quit": [pygame.K_ESCAPE, pygame.K_q],
	"screenshot": [pygame.K_F12],
	"resolution": [pygame.K_F11],
	"fullscreen": [pygame.K_F10],
}

dtcombo = 0.2

