from . import ptext, pview
from .pview import T

done = False

def init():
	global t, done
	t = 0

def control(kpressed, kdowns):
	global done
	if t > 0.5 and "act" in kdowns:
		done = True

def think(dt):
	global t
	t += dt
	
def draw():
	pview.fill((20, 20, 20))
	text = "\n".join([
		"Time was not on your side.",
		"Press Space to try again.",
	])
	ptext.draw(text, center = pview.center, fontsize = T(40), bold = True,
		color = (255, 200, 255), gcolor = (100, 255, 100), owidth = 1)
	

