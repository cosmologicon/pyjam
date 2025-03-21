# Game settings, including command-line options and mechanics.

import os, sys, pygame

gamename = "Faraway Near"
DEBUG = "--DEBUG" in sys.argv

minfps, maxfps = 10, 60
ups = 120

lowres = "--lowfi" in sys.argv

resolutions = 360, 480, 720, 900
res = 480
for arg in sys.argv:
	if arg.startswith("--res="):
		res = int(arg[6:])
forceres = "--forceres" in sys.argv
fullscreen = "--fullscreen" in sys.argv


audio = "--noaudio" not in sys.argv
music = audio and "--nomusic" not in sys.argv
sfx = audio and "--nosfx" not in sys.argv

playspeed = 1
if "--slow" in sys.argv:
	playspeed = 0.75
for arg in sys.argv:
	if arg.startswith("--speed="):
		playspeed = float(arg[8:])

unlock = "--unlock" in sys.argv

# The uniform motion of the camera.
# Don't change this. It will mis-calibrate the position of everything.
speed = 24
# Default position of the player to the left of the center.
lag = 30
# Pixels per game unit at the baseline resolution
gamescale = 10

# Duration before you land when we'll still register a jump if you press and hold jump
# until landing.
prejumptime = 0.2

# Approximate time to reach the cliff when jump is pressed when we'll hold off on jumping
# until the cliff is reached.
cliffhangtime = 0.2

savename = os.path.join("save", "progress.txt")
scorename = os.path.join("save", "hiscore.txt")
try:
	os.makedirs(os.path.dirname(savename))
except OSError:
	pass
try:
	os.makedirs(os.path.dirname(scorename))
except OSError:
	pass
if "--reset" in sys.argv:
	if os.path.exists(savename):
		os.remove(savename)

keys = {
	"jump": [pygame.K_SPACE, pygame.K_RETURN, pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"select": [pygame.K_SPACE, pygame.K_RETURN],
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
}
def isdown(kdowns, keyname):
	return any(key in kdowns for key in keys[keyname])
def ispressed(kpressed, keyname):
	return any(kpressed[key] for key in keys[keyname])

