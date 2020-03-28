import pygame
from . import settings
if not settings.noaudio:
	pygame.mixer.pre_init(22050, -16, 1, 2)
from . import view, pview, ptext, state, control, progress, draw, sound
from . import scene, playscene, mapscene, dialogscene, titlescene
from .pview import T

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
pygame.init()
view.init()
control.init()
draw.killtimeinit()
pygame.display.set_caption(settings.gamename)

scene.push(titlescene)

clock = pygame.time.Clock()
playing = True
sound.playmusic("spotlight")
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	
	current = scene.top()
	for keys in control.get():
		if "quit" in keys:
			playing = False
		elif "screenshot" in keys:
			pview.screenshot()
		elif "fullscreen" in keys:
			if current is playscene:
				sound.play("no")
			else:
				pview.toggle_fullscreen()
				settings.fullscreen = not settings.fullscreen
				draw.killtimeinit()
		elif "resolution" in keys:
			if current is playscene:
				sound.play("no")
			else:
				pview.cycle_height(settings.heights)
				draw.killtimeinit()
		elif current:
			current.control(keys)
		if settings.DEBUG and "unlockall" in keys:
			progress.unlockall()
		if settings.DEBUG and "beatcurrent" in keys:
			if current is playscene:
				state.beatcurrent()
			if current is mapscene:
				progress.beat(progress.at)

	if current:
		current.think(dt)
		current.draw()
	else:
		playing = False

	if settings.DEBUG:
		text = "\n".join([
			"F1: unlock all stages",
			"F2: beat current stage",
			"%.1ffps" % clock.get_fps(),
		])
		ptext.draw(text, bottomleft = pview.bottomleft, fontsize = T(24), owidth = 1)
	pygame.display.flip()


