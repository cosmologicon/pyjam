from . import settings, view, pview, ptext, play, control
import pygame

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "Quantico"

view.init()
play.init()
clock = pygame.time.Clock()
while control.playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	play.think(dt)
	play.draw()
	ptext.draw(f"{clock.get_fps():.1f}fps", bottomright = pview.T(1280, 720), fontsize = pview.T(20))
	pygame.display.flip()

