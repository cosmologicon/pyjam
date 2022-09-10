import pygame
from . import pview, ptext
from . import settings, view, play, sound, control
from .pview import T

ptext.DEFAULT_FONT_NAME = "fonts/PassionOne.ttf"
ptext.DEFAULT_OUTLINE_WIDTH = 0.5
ptext.DEFAULT_SHADOW_OFFSET = 0.2, 0.6
pygame.init()
view.init()
sound.init()
control.init()

clock = pygame.time.Clock()
playing = True
level = 1
play.init(level)
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			for keyname, keycode in settings.keys.items():
				if keycode == event.key:
					kdowns.add(keyname)
	if "quit" in kdowns:
		playing = False
	if "resolution" in kdowns:
		pview.cycle_height(settings.heights)
	if "fullscreen" in kdowns:
		pview.toggle_fullscreen()
	if "screenshot" in kdowns:
		pview.screenshot()

	control.think(dt)
	
	play.think(dt, kdowns)
	
	play.draw()
	
	if "laststage" in kdowns:
		level = max(level - 1, 1)
		play.init(level)
	if play.won() or "nextstage" in kdowns:
		level = min(level + 1, 3)
		play.init(level)
	
	if settings.DEBUG:
		text = "\n".join([
			f"{100 * play.self.dmap.fwater():.1f}%",
			f"{clock.get_fps():.1f}fps",
		])
		ptext.draw(text, bottomleft = pview.bottomleft, owidth = 1,
			fontsize = T(26))
	pygame.display.flip()


