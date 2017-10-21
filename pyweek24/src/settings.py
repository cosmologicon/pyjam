import os, sys, pygame

gamename = "They're Behind Everything"
DEBUG = "--DEBUG" in sys.argv

minfps, maxfps = 10, 60

lowres = "--lowres" in sys.argv

resolutions = 360, 480, 720, 900

res = 480


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
try:
	os.makedirs(os.path.dirname(savename))
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

