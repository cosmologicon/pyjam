import pygame, math
from . import maff, view, pview, ptext, hill
from .pview import T

specs = {
	"island": (
		((-10, 1), (-5, 3), (5, 3), (10, 1)),
		((-7, -3), (0, -5), (7, -3)),
		((0, -7),),
	),
}

hills = []
jcursor = -1

view.init()
clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(20)
	kdowns = []
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			kdowns.append(event.key)
		if event.type == pygame.QUIT:
			playing = False
	kpressed = pygame.key.get_pressed()
	step = 0.125 if kpressed[pygame.K_LSHIFT] else 1

	if pygame.K_F11 in kdowns:
		pview.toggle_fullscreen()
	if pygame.K_RETURN in kdowns:
		jcursor = len(hills)
		hills.append({
			"specname": "island",
			"x": 0,
			"y": 0,
			"z": 0,
		})
	if pygame.K_a in kdowns:
		hills[jcursor]["x"] -= step
	if pygame.K_e in kdowns:
		hills[jcursor]["x"] += step
	if pygame.K_o in kdowns:
		hills[jcursor]["y"] -= step
	if pygame.K_COMMA in kdowns:
		hills[jcursor]["y"] += step
	if pygame.K_QUOTE in kdowns:
		hills[jcursor]["z"] -= step
	if pygame.K_PERIOD in kdowns:
		hills[jcursor]["z"] += step
	if kpressed[pygame.K_RIGHT]:
		view.X0 += 16 * step * dt
	if kpressed[pygame.K_LEFT]:
		view.X0 -= 16 * step * dt
	pview.fill((0, 0, 0))
	for jhill in sorted(range(len(hills)), key = lambda jhill: hills[jhill]["z"]):
		if jhill == jcursor and pygame.time.get_ticks() % 500 > 400:
			continue
		h = hills[jhill]
		hill.drawhill((h["x"], h["y"], h["z"]), specs[h["specname"]])
	for h in hills:
		px, py = view.toscreen(h["x"], h["y"], h["z"])
		pygame.draw.circle(pview.screen, (255, 255, 255), (px, py), T(2))
	ptext.draw("%.1ffps" % clock.get_fps(), bottomleft = T(10, 470), fontsize = T(16))

	pygame.display.flip()
	if pygame.K_ESCAPE in kdowns:
		playing = False


