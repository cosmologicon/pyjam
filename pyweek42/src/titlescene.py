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
	text = "TIMESTEALER\n\nA mad scientist has created a superweapon called the Timestealer, with the power to borrow Time from one part of the continuum and place it in another part. You have boarded the villain's space station and acquired the Timestealer. Now you must use the its ablities to escape with your life.\n\nPress Space to begin."
	ptext.draw(text, center = pview.center, fontsize = T(30), width = T(1000), bold = True,
		color = (255, 200, 255), gcolor = (100, 255, 100), owidth = 1)
	

