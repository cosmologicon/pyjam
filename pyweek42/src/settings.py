import pygame

gamename = "Borrowed Time"

size0 = 1280, 720
height = 720
heights = 480, 540, 720, 1080, 1440
fullscreen = False
forceres = False

minfps, maxfps = 5, 120
dt0 = 0.008

DEBUG = True

controls = {
	"quit": [pygame.K_ESCAPE],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"resolution": [pygame.K_F10],
	"fullscreen": [pygame.K_F11],
	"screenshot": [pygame.K_F12],
}

