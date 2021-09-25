import pygame, math, random
from . import view, pview, graphics, geometry, state, ptext, progress, settings, scene, profiler, sound
from .pview import T

class self:
	pass


def init():
	self.t = 0
	self.twin = 0
	self.started = False
	self.snap = True
	if scene.current == "adventure":
		state.adventure_init()
		sound.playmusic("brittle")
	elif scene.current == "endless":
		state.endless_init()
		sound.playmusic("destiny")
	from . import gameoverscene
	gameoverscene.init()

def winning():
	if scene.current == "adventure":
		return state.adventure_winning()
	elif scene.current == "endless":
		return state.endless_winning()
	

def getvtarget():
	if settings.fixedcamera:
		return state.adventure_vtarget() if scene.current == "adventure" else state.endless_vtarget()
	if winning():
		return state.adventure_vtarget() if scene.current == "adventure" else state.endless_vtarget()
	elif state.gameover():
		return state.you.pos, 200
	elif state.you.chompin:
		return state.you.vtarget, state.you.starget
	else:
		return state.you.pos, 40

def reset():
	self.snap = True


def think(dt, kpressed, kdowns):
	self.t += dt

	if "quit" in kdowns:
		self.started = False
		if scene.current in ["adventure", "endless"]:
			scene.setcurrent("settings_" + scene.current)

	if "act" in kdowns:
		if not self.started:
			self.started = True
		elif not state.you.chompin and state.you.canchomp() and state.you.tchomp == 0:
			state.you.chomp()
		elif state.you.chompin:
			state.you.unchomp()
	
	dkx = (1 if kpressed["right"] else 0) - (1 if kpressed["left"] else 0)
	dky = (1 if kpressed["up"] else 0) - (1 if kpressed["down"] else 0)

	if state.gameover():
		if scene.current in ["adventure", "endless"]:
			sound.playsound("gameover")
			scene.setcurrent("gameover_" + scene.current)
	if self.started and not state.gameover():
		if winning():
			dkx, dky = 0, 0
		if not (scene.current == "endless" and state.endless_winning()):
			state.you.think(dt, dkx, dky)
	if scene.current == "adventure":
		state.adventure_think(dt)
	elif scene.current == "endless":
		state.endless_think(dt)

	vtarget, starget = getvtarget()
	if self.snap:
		(view.x0, view.y0), view.scale = vtarget, starget
		self.snap = False
	else:
		view.x0, view.y0 = math.softapproach((view.x0, view.y0), vtarget, 4 * dt, dymin=0.001)
		view.scale = math.softlogapproach(view.scale, starget, 1 * dt, dymin=0.001)

	if winning():
		self.twin += dt
	if scene.current == "endless" and self.twin > 1:
		progress.beatendless(state.stage)
		init()
	if scene.current == "adventure" and self.twin > 8:
		progress.resetadventure()
		scene.setcurrent("menu")
		

def draw():
	profiler.start("stardraw")
	graphics.drawstars()
	profiler.stop("stardraw")
	profiler.start("youdraw")
	state.you.draw()
	profiler.stop("youdraw")
	profiler.start("walldraw")
	state.drawwalls()
	profiler.stop("walldraw")
	for obj in state.objs:
		if obj.visible():
			obj.draw()		
	for effect in state.effects:
		effect.draw()
	if scene.current == "adventure":
		drawadventurehud()
	elif scene.current == "endless":
		drawendlesshud()


def drawadventurehud():
	infos = {
		1: ("Space/Enter: begin\nArrows/WASD: move\nEsc: help/settings/quit", "bottomleft"),
		2: ("F1: toggle control scheme\n[%s]\nAbsolute is like traditional Snake. Relative is a little more precise once you get the hang of it." %
				("absolute" if settings.directcontrol else "relative"), "bottomright"),
		3: ("F2: toggle camera\n[%s]" % ("fixed" if settings.fixedcamera else "follow"), "topleft"),
		4: ("Space/Enter: bite your own tail. Encircle (go around) the object and bite your tail to unlock the next area.", "topright"),
		5: ("This key is rotating. You must encircle it going clockwise to unlock it.", "topleft"),
		6: ("This one must be encircled counterclockwise.", "bottomright"),
		7: ("F3: toggle auto-bite\n[%s]" % ("on" if settings.autochomp else "off"), "midright"),
		8: ("Energy increases your length. Encircle to collect it.", "bottomleft"),
		12: ("Encircle both keys at the same time. A number on a key tells you how many keys must be encircled at the same time as it.", "bottomright"),
		13: ("You must encircle them both at the same time in different directions. This calls for a Figure 8.", "topleft"),
		15: ("Disruptors can't be activated, and they prevent you from activating energy and keys. Encircle the energy without including any of the disruptors.", "topleft"),
		16: ("It's fine to encircle walls if they don't contain a disruptor.", "topleft"),
		21: ("Remember, you need to encircle all three keys but not the disruptor.", "bottomright"),
		22: ("Remember, it's fine to encircle walls", "midleft"),
		25: ("Thank you for playing.", "midbottom"),
	}
	rect = pygame.Rect(T(240, 160, pview.w0 - 480, pview.h0 - 320))
	if state.stage in infos:
		text, edge = infos[state.stage]
		pos = getattr(rect, edge)
		ptext.draw(text, center = pos, fontsize = T(32), width = T(400),
			owidth = 0.5, color = (128, 240, 255), shade = 1)

	a = int(math.smoothfadebetween(self.twin, 7.5, 0, 8, 255))
	if a > 0:
		pview.fill((20, 60, 120, a))

	


def drawendlesshud():
	ptext.draw("Stage %s" % state.stage, topleft = T(20, 20), fontsize = T(60), owidth = 0.5, shade = 1)



