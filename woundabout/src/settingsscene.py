import pygame, math
from . import scene, playscene, view, pview, ptext, settings, graphics, snek, geometry, state, menuscene
from .pview import T


class self:
	pass

def init():
	self.t = 0
	self.done = False
	self.tdone = 0
	self.objs = [
		state.GrowStar((0, 4.4), display = True),
		state.Star((0, 2.7), r = 0.5, display = True),
		state.Star((0, 0.6), r = 0.5, windreq = -1, display = True),
		state.Star((0, -1.8), r = 0.5, numreq = 3, display = True),
		state.Star((0, -4.3), r = 0.5, numreq = -1, display = True),
	]
		

def think(dt, kpressed, kdowns):
	self.t += dt
	for obj in self.objs:
		obj.think(dt)	
	if self.done:
		self.tdone += dt
		if self.tdone > 0.2:
			finish()
	else:
		if "act" in kdowns:
			self.done = True
	if "quit" in kdowns:
		scene.setcurrent("menu")

def finish():
	if scene.current == "settings_menu":
		menuscene.reset()
		scene.setcurrent("menu", False)
	if scene.current == "settings_endless":
		playscene.reset()
		scene.setcurrent("endless", False)
	if scene.current == "settings_adventure":
		playscene.reset()
		scene.setcurrent("adventure", False)
	

def draw():
	pview.fill((0, 20, 50))
	view.x0, view.y0, view.scale = 0, 0.3, 46
	for obj in self.objs:
		obj.draw()
	optnames = "\n".join([
		"Arrows or WASD: move",
		"Space or Enter: bite/release",
		"F1: controls [%s]" % ("absolute" if settings.directcontrol else "relative"),
		"F2: camera [%s]" % ("fixed" if settings.fixedcamera else "follow"),
		"F3: auto-bite [%s]" % ("on" if settings.autochomp else "off"),
		"F4: sfx volume [%d%%]" % settings.sfxvolume,
		"F5: music volume [%d%%]" % settings.musicvolume,
		"F10: resolution [%dp]" % settings.height,
		"F11: fullscreen",
		"F12: screenshot",
		"Esc: quit",
	])
	ptext.draw(optnames, topleft = T(40, 80), fontsize = T(40), owidth = 0.5, shade = 1)

	helptext = "Encircle objects to activate them."
	ptext.draw(helptext, topleft = T(600, 80), width = T(600), fontsize = T(40), shadow = (1, 1), shade = 1)

	text = "\n".join([
		"Energy: grow",
		"Key: unlock",
		"Directional key: must encircle in the correct direction to unlock.",
		"Numbered key: must unlock at least this many at the same time.",
		"Disruptor: cannot be activated. Prevents activating other objects.",
	])
	ptext.draw(text, topleft = T(700, 150), width = T(500), fontsize = T(34), shadow = (1, 1),
		shade = 1, pspace = 0.7)

	ptext.draw("Space/Enter: back", midbottom = T(640, 700), fontsize = T(34), shadow = (1, 1),
		shade = 1)

	alpha = math.imix(0, 255, math.fadebetween(self.tdone, 0, 0, 0.1, 1))
	if alpha > 0:
		pview.fill((20, 60, 120, alpha))


