import math, pygame
from . import ptext, pview, state
from .pview import T


def init():
	pass

def think(dt):
	pass

def draw():
	helptext = None
	if state.current_stage == 1 and state.tstage < 10:
		helptext = "Arrows or WASD: avoid the hazards"
	if state.current_stage == 2 and state.tstage < 10:
		helptext = "Space or Enter: Discharge or charge the Timestealer"
	if helptext is not None:
		ptext.draw(helptext, midbottom = T(640, 700), width = T(900), fontsize = T(40), bold = True,
			color = (255, 200, 255), gcolor = (100, 255, 100), owidth = 1)
	text = f"Current stage: {state.current_stage}\nHealth: {state.health}/3"
	ptext.draw(text, topright = T(1270, 10), fontsize = T(32), bold = False,
		color = (255, 200, 255), gcolor = (100, 255, 100), owidth = 1)

	ptext.draw("Timestealer\ncharge", midtop = T(1200, 500), fontsize = T(25), bold = True,
		color = (255, 200, 255), gcolor = (100, 255, 100), owidth = 1)
	
	rect0 = pygame.Rect(0, 0, 30, 200)
	rect1 = rect0.copy()
	rect1.height = math.mixI(0, rect0.height, state.device.charge)
	rect0.midbottom = 1200, 490
	rect1.midbottom = rect0.midbottom
	
	pygame.draw.rect(pview.screen, (255, 100, 255), T(rect1))
	pygame.draw.rect(pview.screen, (100, 100, 100), T(rect0), T(5))


