from pygame.locals import *

gamename = "Lesser of Two Evils"

minfps = 5
maxfps = 120

DEBUG = True

fullscreen = False
windowsize = 480  # 16:9 aspect ratio

screenshotdir = "screenshots"

swapaction = False

controls = {
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"action": [K_SPACE, K_RETURN, K_LCTRL, K_RCTRL, K_LSHIFT, K_RSHIFT, K_z],
	"swap": [K_CAPSLOCK, K_TAB],
	"quit": [K_ESCAPE, K_q],
	"fullscreen": [K_F11, K_f],
	"screenshot": [K_F12],
}
def isdown(key, kdowns):
	return any(k in kdowns for k in controls[key])
def ispressed(key, kpressed):
	return any(kpressed[k] for k in controls[key])

