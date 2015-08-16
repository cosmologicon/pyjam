from __future__ import division
# import vidcap
import pygame, datetime, os.path
from pygame.locals import *
from src import settings, thing, window, ptext, state, background, scene, sound
from src.window import F
from src.scenes import play, intro, title, finalcutscene, endtitle

ptext.FONT_NAME_TEMPLATE = os.path.join("data", "fonts", "%s.ttf")

window.init()
pygame.display.set_caption(settings.gamename)
pygame.mixer.init()
background.init()
sound.init()

if os.path.exists(settings.savename):
	scene.current = play
	scene.toinit = None
	sound.playgamemusic()
	background.wash()
	state.load()
else:
#	sound.playgamemusic()
#	from src import quest
#	quest.quests["Finale"].setup()
#	scene.current = finalcutscene
#	scene.toinit = finalcutscene
#	scene.current = endtitle
#	scene.toinit = endtitle
	scene.current = intro
	scene.toinit = intro
	title.drawtitle()

clock = pygame.time.Clock()
playing = True
tconfirmfull = 0
while playing:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	class Event(object):
		def __init__(self, event):
			self.type = event.type
			if event.type in (KEYDOWN, KEYUP):
				self.key = event.key
				for keyname, codes in settings.keycodes.items():
					if event.key in codes:
						self.key = keyname
	events = list(map(Event, pygame.event.get()))
	for event in events:
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN and event.key == "quit":
			playing = False
		if event.type == KEYDOWN and event.key == K_F11:
			settings.fullscreen = not settings.fullscreen
			if settings.fullscreen:
				tconfirmfull = 10
			window.init()
			if scene.current == intro:
				title.drawtitle()
		if event.type == KEYUP and event.key == "go":
			tconfirmfull = 0
		if event.type == KEYDOWN and event.key == "screenshot":
			fname = datetime.datetime.now().strftime("screenshot-%Y%m%d%H%M%S.png")
			pygame.image.save(window.screen, os.path.join("screenshots", fname))
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F2:
			print("things %d" % (len(thing.things)))
			print("ships %d %d" % (len(state.ships), sum(map(window.camera.on, state.ships))))
			print("objs %d %d" % (len(state.objs), sum(map(window.camera.on, state.objs))))
			print("hazards %d %d" % (len(state.hazards), sum(map(window.camera.on, state.hazards))))
			print("effects %d %d" % (len(state.effects), sum(map(window.camera.on, state.effects))))
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F3:
			settings.drawbackground = not settings.drawbackground
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F4:
			state.you.y = 100
			state.you.hp += 100
		if event.type == KEYDOWN and event.key == "save" and scene.current is play:
			state.save()
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F6:
			scene.current = title
			scene.toinit = title
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F7:
			scene.current = play
			play.init()
			background.wash()
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F9:
			from src.scenes import act2cutscene
			from src import scene
			scene.current = act2cutscene
			scene.toinit = act2cutscene
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_KP0:
			sound.epicness = 0
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_KP1:
			sound.epicness = 1
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_KP2:
			sound.epicness = 2


	kpressed = pygame.key.get_pressed()
	if settings.DEBUG and kpressed[K_1]:
		dt *= 3
	kpressed = {
		keyname: any(kpressed[code] for code in codes)
		for keyname, codes in settings.keycodes.items()
	}
	if scene.toinit:
		scene.toinit.init()
		scene.toinit = None
	s = scene.current
	if not s:
		break
	if tconfirmfull:
		if tconfirmfull == 10:
			s.think(0, events, kpressed)
		s.draw()
		ptext.draw("Press space to\nconfirm fullscreen", fontsize = F(50), owidth = 1,
			center = window.screen.get_rect().center, fontname = "Orbitron", color = "orange")
		tconfirmfull -= dt
		if tconfirmfull <= 0:
			settings.fullscreen = False
			window.init()
			tconfirmfull = 0
	else:
		s.think(dt, events, kpressed)
		s.draw()
	if settings.DEBUG:
		if state.you:
			ptext.draw("%.4f, %.1f" % (state.you.X, state.you.y), fontsize = F(36),
				bottomright = (window.sx - F(10), window.sy - F(50)), cache = False)
		ptext.draw("%.1ffps" % clock.get_fps(), fontsize = F(36),
			bottomright = (window.sx - F(10), window.sy - F(10)), cache = False)
	pygame.display.flip()

if scene.current is play and settings.saveonquit:
	state.save()
pygame.quit()

