import pygame, math, os
from . import settings, pview, view, ptext, sound
from . import playscene
from .pview import T

ptext.FONT_NAME_TEMPLATE = os.path.join("fonts", "%s.ttf")
view.init()
sound.init()
level = 1
playscene.init(level)
scene = playscene

playing = True
dtaccum = 0
clock = pygame.time.Clock()
while playing:

	dt0 = 1 / settings.maxfps
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	dtaccum += dt
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			kdowns.add(settings.keys_by_code.get(event.key))

	kpressed = pygame.key.get_pressed()
	kpressed = { key: any(kpressed[code] for code in codes) for key, codes in settings.keys.items() }
	kdx = kpressed["right"] - kpressed["left"]
	kdy = kpressed["up"] - kpressed["down"]
	if kdx or kdy:
		kdx, kdy = math.norm((kdx, kdy), dt * settings.walkspeed)
	ktip = kpressed["tip"] * dt
	scene.control(kdowns, kdx, kdy, ktip)
	view.setzoomout(kpressed["zoomout"], dt)
	
	while dtaccum > 0:
		scene.think(dt0)
		dtaccum -= dt0
	scene.draw()
	
	if settings.DEBUG:
		text = "\n".join([
			"%.1ffps" % clock.get_fps(),
		])
		ptext.draw(text, fontsize = T(30), owidth = T(2), bottomleft = T(0, 720))


	pygame.display.flip()

	if "quit" in kdowns:
		playing = False
	if playscene.done():
		level += 1
		playscene.init(level)
	elif "next" in kdowns:
		sound.play("skip")
		level += 1
		playscene.init(level)
	elif "prev" in kdowns:
		sound.play("skip")
		level = max(level - 1, 1)
		playscene.init(level)



