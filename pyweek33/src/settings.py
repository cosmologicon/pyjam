import pygame

gamename = "My Evil Twin"

minfps = 5
maxfps = 120
DEBUG = True

keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"act": [pygame.K_SPACE],
	"quit": [pygame.K_ESCAPE],
	"screenshot": [pygame.K_F12],
}
keys_by_code = { code: keyname for keyname, codes in keys.items() for code in codes }	

fullscreen = False
size0 = 1280, 720
heights = 480, 600, 720, 1080

