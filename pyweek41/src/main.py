from . import settings, view, pview, ptext, play, control, sound, world
import pygame

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "Quantico"

view.init()
play.init()
pygame.mixer.init()
sound.playmusic()
clock = pygame.time.Clock()
while control.playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	play.think(dt)
	sound.think(dt)
	play.draw()
	pygame.display.flip()

if settings.editor:
	world.dumpstars()
