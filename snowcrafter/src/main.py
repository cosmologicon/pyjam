from __future__ import division
import pygame
from . import settings, control, view, pview, ptext, background, client, progress, sound
from . import scene, playscene, menuscene, storyscene
from .pview import T

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
pview.SCREENSHOT_DIRECTORY = "screenshot"
view.init()
pygame.mixer.init()
if progress.canload() and not settings.reset:
	progress.load()
sound.playmusic("undaunted")
if progress.donestory:
	scene.push(menuscene, "main")
else:
	scene.push(menuscene, "main")
	scene.push(playscene, "stage%d" % progress.stage)
	scene.push(storyscene, "stage%d" % progress.stage)

client.pullgallery()

playing = True
clock = pygame.time.Clock()
taccum = 0
while playing:
	dt = min(0.001 * clock.tick(settings.ups), 1 / 10)
	taccum += dt
	controls = control.Controls()
	if controls.quit:
		playing = False
	if pygame.K_F10 in controls.kdowns:
		pview.cycle_height(settings.heights)
		settings.height = pview.height
		settings.save()
		background.clear()
	if pygame.K_F11 in controls.kdowns:
		settings.fullscreen = not settings.fullscreen
		settings.save()
		pview.toggle_fullscreen()
		background.clear()
	if pygame.K_F12 in controls.kdowns:
		pview.screenshot()

	current = scene.top()
	if current is None:
		break
	dt0 = 1 / settings.ups
	while taccum > 0.5 * dt0:
		current.think(dt0, controls)
		controls.clear()
		taccum -= dt0
	current.draw()

	if settings.DEBUG:
		text = "%.1fps %s" % (clock.get_fps(), pygame.mouse.get_pos())
		ptext.draw(text, bottomleft = T(10, 710), fontsize = T(30), owidth = 1.2)
	pygame.display.flip()
pygame.quit()

