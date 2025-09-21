import pygame
from . import ptext
from . import settings, view, play, control
from .pview import T

view.init()
control.init()

while control.playing():
	control.tick()
	for dt in control.dts():
		play.think(dt)
	play.draw()
	ptext.draw(control.infotext(), bottomleft = T(10, 790), fontsize = T(30))
	pygame.display.flip()




