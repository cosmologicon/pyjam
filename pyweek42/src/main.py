import pygame, os.path
from . import settings, view, pview, playscene, ptext, state, sound, hud, endscene, diescene, titlescene

ptext.DEFAULT_FONT_NAME = os.path.join("font", "Asimovian.ttf")
pygame.init()
view.init()
sound.init()
hud.init()
titlescene.init()

playing = True
clock = pygame.time.Clock()
dtaccum = 0
scene = titlescene
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	sound.think(dt)
	hud.think(dt)
	
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			for k, keys in settings.controls.items():
				if event.key in keys:
					kdowns.add(k)
	if "quit" in kdowns: playing = False
	if "fullscreen" in kdowns: pview.toggle_fullscreen()
	if "resolution" in kdowns: pview.cycle_height(settings.heights)
	if "screenshot" in kdowns: pview.screenshot()
	
	kpressed0 = pygame.key.get_pressed()
	kpressed = set(k for k, keys in settings.controls.items() if any(kpressed0[key] for key in keys))

	scene.control(kpressed, kdowns)
	dtaccum += dt * state.tfactor()
	while dtaccum >= settings.dt0:
		dtaccum -= settings.dt0
		scene.think(settings.dt0)
	
	scene.draw()
	if settings.DEBUG:
		text = "\n".join([
			f"stage {state.current_stage}",
			f"tstage {state.tstage:.1f}",
			f"tfactor: {state.tfactor()}",
			f"{clock.get_fps():.1f}fps",
		])
		ptext.draw(text, bottomleft = pview.bottomleft, fontsize = pview.T(35),
			owidth = 1)
	pygame.display.flip()

	if scene is titlescene and titlescene.done:
		scene = playscene
		playscene.init()
	if scene is playscene and state.won:
		scene = endscene
		endscene.init()
	if scene is playscene and state.health == 0:
		scene = diescene
		diescene.init()
	if scene is endscene and endscene.done:
		playing = False
	if scene is diescene and diescene.done:
		scene = playscene
		playscene.init()
	
	



