from pygame.locals import *
import sys, os

DEBUG = True  # TODO: change to False before submitting
# TODO: empty savegame subdirectory before submitting

gamename = "Flow"

resolution = 1024, 720
fullscreen = "--fullscreen" in sys.argv

leveldataname = "leveldata"

maxfps = 120
minfps = 10

savename = os.path.join("savegame", "save.pkl")
asavename = os.path.join("savegame", "save-%Y%m%d%H%M%S.pkl")

debug_graphics = "--debuggfx" in sys.argv

for arg in sys.argv:
	if "=" in arg:
		oname, ovalue = arg.lstrip("-").split("=")
		if oname == "level":
			leveldataname = ovalue

keymap = {
	# Dvorak key layout too.
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	"turn": [K_LSHIFT, K_z, K_SEMICOLON],
	"act": [K_SPACE, K_RETURN],
	
	"quit": [K_ESCAPE],
	
	"debugspeed": [K_F1],
}

