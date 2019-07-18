import pygame
from . import vista, state, button, scene, buildscene, dialog, img, settings, sound, quest
from .settings import F

apart = {
	"mother": False,
}
shroud = None
mapmode = False

def init():
	makebuttons()
	apart["mother"] = False

buttons = []
brects = [
	F(667 - 125 if j < 5 else 667 + 5, 50 + j % 5 * 34, 120, 30)
	for j in range(10)
]
def makebuttons():
	del buttons[:]
	for j, bname in enumerate(state.state.modules):
		if bname in state.state.hookup:
			buttons.append(button.ModuleButton(bname, brects[j], fontsize = F(18)))

def handleclick(pos):
	for b in buttons:
		if b.within(pos):
			b.click()
			return
	worldpos = vista.screentoworld(pos)
	state.state.you.target = worldpos


def think(dt, events, mpos):
	sound.playmusic("boss" if state.state.bossmode else "travel")
	if settings.pauseondialog and state.state.playing:
		dialog.think(dt)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and state.state.tline > 0.5:
				dialog.advance()
		dt = 0

	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			handleclick(event.pos)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F1 and settings.DEBUG:
			scene.push(buildscene)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F2 and settings.DEBUG:
			state.state.you.x = state.state.mother.x
			state.state.you.y = state.state.mother.y
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F3 and settings.DEBUG:
			state.state.bank += 1
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and settings.DEBUG:
			state.state.bank += 10
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F5 and settings.DEBUG:
			state.state.bank += 100
	global mapmode
	mapmode = any(b.name == "scope" and b.within(mpos) for b in buttons)

	state.state.think(dt)
	vista.think(dt)
	dialog.think(dt)
	for b in buttons:
		b.think(dt)

	if state.state.mother.within((state.state.you.x, state.state.you.y)):
		if apart["mother"]:
			apart["mother"] = False
			scene.push(buildscene)
			state.state.you.x = state.state.mother.x
			state.state.you.y = state.state.mother.y
			state.state.you.allstop()
	else:
		apart["mother"] = True

	global shroud
	if shroud:
		alpha = shroud.get_alpha()
		alpha = int(alpha - 200 * dt)
		if alpha <= 0:
			shroud = None
		else:
			shroud.set_alpha(alpha)
	if not state.state.you.corpse.alive:
		import menuscene
		scene.pop()
		scene.push(menuscene)

def setshroud(color, alpha = 255):
	global shroud
	if shroud is None:
		shroud = pygame.Surface(settings.ssize).convert()
	shroud.fill(color)
	shroud.set_alpha(alpha)


def draw():
	if mapmode:
		state.state.drawmainmap()
	else:
		state.state.drawviewport()
	vista.screen.fill((20, 25, 30), settings.prect)
	state.state.drawnavmap()
	if state.state.alerts:
		img.drawtext("\n".join(state.state.alerts), color = (255, 0, 0), fontsize = settings.alertfontsize, topleft = (0, 0))
	for b in buttons:
		b.draw()
	img.drawtext("Connected modules:", fontsize = F(24), fontname = "prosto", topleft = F(490, 10))
	texts = [
		"SpaceBucks: %s" % state.state.bank,
		"Hull: %s/%s" % (state.state.you.hp, state.state.you.maxhp),
	]
	colors = [
		(200, 200, 200),
		(100, 200, 100),
	]
	for j, (text, color, pos) in enumerate(zip(texts, colors, settings.statpos)):
		img.drawtext(text, fontsize = settings.statfontsize, fontname = "prosto", center = pos)
	if shroud:
		vista.screen.blit(shroud, (0, 0))
	dialog.draw()


