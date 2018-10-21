from pygame.locals import *
import sys

DEBUG = True  # TODO: change to False before submitting

gamename = "Flow"

resolution = 854, 480
fullscreen = "--fullscreen" in sys.argv

maxfps = 120

keymap = {
	# Dvorak key layout too.
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	"turn": [K_LSHIFT, K_z, K_SEMICOLON],
	
	"quit": [K_ESCAPE],
}

