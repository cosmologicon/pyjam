import pygame
from . import settings, view, ptext, state, pview, profiler, sound
from . import scene, playscene, gameoverscene, menuscene, settingsscene
from .pview import T

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "berkshire"
settings.load()
view.init()

scene.setcurrent("menu")

playing = True
clock = pygame.time.Clock()
dtaccum = 0
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			kdowns.add(event.key)
	kpressed = pygame.key.get_pressed()
	kdowns, kpressed = settings.remapkeys(kdowns, kpressed)


	if settings.DEBUG and "quit" in kdowns:
		playing = False
	if settings.DEBUG and "cheatwin" in kdowns:
		state.cheatwin()
	if settings.DEBUG and "cheatgrow" in kdowns:
		state.cheatgrow()
	if "controls" in kdowns:
		settings.directcontrol = not settings.directcontrol
		settings.save()
	if "camera" in kdowns:
		settings.fixedcamera = not settings.fixedcamera
		settings.save()
	if "chomp" in kdowns:
		settings.autochomp = not settings.autochomp
		settings.save()
	if "sfx" in kdowns:
		sound.cycle_sfxvolume()
	if "music" in kdowns:
		sound.cycle_musicvolume()
	if "resize" in kdowns:
		view.resize()
	if "fullscreen" in kdowns:
		view.toggle_fullscreen()
	if "screenshot" in kdowns:
		pview.screenshot()
	current = scene.current

	if scene.toinit:
		scene.toinit = False
		if current == "menu":
			menuscene.init()
		if current in ["adventure", "endless"]:
			playscene.init()
		if "settings" in current:
			settingsscene.init()


	profiler.start("think")
	dtaccum += dt
	dt0 = 1 / settings.maxfps
	while dtaccum > dt0:
		dtaccum -= dt0
		if current in ["adventure", "endless"]:
			playscene.think(dt0, kpressed, kdowns)
	if current == "gameover":
		gameoverscene.think(dt, kpressed, kdowns)
	if current == "menu":
		menuscene.think(dt, kpressed, kdowns)
	if "settings" in current:
		settingsscene.think(dt, kpressed, kdowns)
	profiler.stop("think")

	view.clear()

	profiler.start("draw")
	if current == "menu":
		menuscene.draw()
	if current in ["adventure", "endless"]:
		playscene.draw()
	if current == "gameover":
		gameoverscene.draw()
	if "settings" in current:
		settingsscene.draw()
	profiler.stop("draw")
	if settings.DEBUG:
		text = "\n".join([
			"1: beat current",
			"2: grow",
			"%.1ffps" % clock.get_fps(),
			profiler.status(),
		])
		ptext.draw(text, bottomleft = T(4, 716), fontsize = T(16))
	pygame.display.flip()


