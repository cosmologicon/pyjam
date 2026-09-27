from . import ptext, pview
from .pview import T

done = False

def init():
	global t, done
	t = 0

def control(kpressed, kdowns):
	pass

def think(dt):
	global t
	t += dt
	
def draw():
	pview.fill((20, 20, 20))
	text = "\n".join([
		"You have escaped and destroyed the Timestealer",
		"to stop it from falling into the wrong hands.",
		"The galaxy is safe once again.",
		"Thank you for playing. Esc to quit.",
	])
	ptext.draw(text, center = pview.center, fontsize = T(40), bold = True,
		color = (255, 200, 255), gcolor = (100, 255, 100), owidth = 1)
	

