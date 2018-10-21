from pygame.locals import *

DEBUG = True  # TODO: change to False before submitting

gamename = "Flow"

resolution = 854, 480

maxfps = 120

keymap = {
	# Dvorak key layout too.
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	
	"quit": [K_ESCAPE],
}

