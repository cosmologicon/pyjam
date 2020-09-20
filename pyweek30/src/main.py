import pygame
from . import settings, view, ptextgl, control, graphics, pview, world

import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


view.init()

pygame.init()
view.init()
control.init()
graphics.init()

playing = True
clock = pygame.time.Clock()
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns, kpressed = control.get()
	if "quit" in kdowns:
		playing = False


	view.clear()
	
	dstep = kpressed["up"] - kpressed["down"]
	drot = kpressed["left"] - kpressed["right"]
	world.step(50 * dt * dstep)
	world.rotate(2 * dt * drot)
	graphics.draw()
	ptextgl.draw("%.1ffps" % clock.get_fps(), (10, 10))
	pygame.display.flip()

pygame.quit()

