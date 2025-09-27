import pygame
from . import ptext
from . import sound, settings, view, play, control, ptext
from .pview import T

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "JockeyOne"

sound.init()
view.init()
play.init()
control.init()

while control.playing():
	control.tick()
	for dt in control.dts():
		play.think(dt)
	play.draw()
	control.drawinfo()
	pygame.display.flip()




