import pygame, math, random
from . import view, pview, graphics, geometry, state, ptext, progress, settings
from .pview import T

class self:
	pass


def init():
	self.t = 0
	self.twin = 0
	self.started = False
	state.adventure_init()
	(view.x0, view.y0), view.scale = getvtarget()
	from . import gameoverscene
	gameoverscene.init()

def getvtarget():
	if settings.fixedcamera:
		return state.vtarget()
	if state.winning():
		return state.vtarget()
	elif state.gameover():
		return state.you.pos, 200
	elif state.you.chompin:
		return state.you.vtarget, state.you.starget
	else:
		return state.you.pos, 40


def think(dt, kpressed, kdowns):
	self.t += dt

	if pygame.K_SPACE in kdowns:
		if not self.started:
			self.started = True
		elif not state.you.chompin and state.you.canchomp() and state.you.tchomp == 0:
			state.you.chomp()
		elif state.you.chompin:
			state.you.unchomp()
	
	dkx = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	dky = (1 if kpressed[pygame.K_UP] else 0) - (1 if kpressed[pygame.K_DOWN] else 0)

#	if self.started and not state.winning() and not state.gameover():
#		state.you.think(dt, dkx, dky)
	if self.started and not state.gameover():
		if state.winning():
			dkx, dky = 0, 0
		state.you.think(dt, dkx, dky)
	state.think(dt)

	vtarget, starget = getvtarget()
	view.x0, view.y0 = math.softapproach((view.x0, view.y0), vtarget, 4 * dt, dymin=0.001)
	view.scale = math.softlogapproach(view.scale, starget, 1 * dt, dymin=0.001)

	if state.winning():
		self.twin += dt
	if self.twin > 8:
		progress.beatendless(state.stage)
		init()
		

def draw():
#	if self.chompin:
#		pview.fill((40, 0, 0))
	graphics.drawstars()
	state.you.draw()
	state.drawwalls()
	for obj in state.objs:
		if obj.visible():
			obj.draw()		

	a = math.smoothfadebetween(self.t, 1.5, 1, 2, 0)
	if a > 0:
		ptext.draw("Endless Stage %s" % state.stage, midbottom = T(640, 700), fontsize = T(60),
			owidth = 1, alpha = a)



