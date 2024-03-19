import pygame

gamename = "Space Age Tube"

minfps, maxfps = 10, 120

keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"act": [pygame.K_SPACE, pygame.K_RETURN],
	"remove": [pygame.K_BACKSPACE, pygame.K_DELETE],
}



size0 = 1280, 720
height = None
fullscreen = False
forceres = False

colors = {
	"R": [255, 50, 50],
	"O": [255, 150, 0],
	"Y": [222, 222, 0],
	"G": [50, 255, 50],
	"B": [80, 80, 255],
	"V": [200, 0, 255],
}

