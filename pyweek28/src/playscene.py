from __future__ import division
import pygame, math
from . import scene, pview, view, ptext, draw, state, worldmap, things, dialog, quest
from .pview import T

class PlayScene(scene.Scene):
	def __init__(self):
		# Where the camera wants to be.
		self.targetyG0 = view.yG0
		self.ftarget = 0
		
		state.stations = [
			things.Station("LowOrbiton", 400),
			things.Station("Skyburg", 2000),
			things.Station("Last Ditch", 3700),
			things.Station("Stationary", 7200),
			things.Station("Counterweight", 10000),
		]
		state.stations[3].addquest("testquest")

		self.up = [pygame.K_UP, pygame.K_w]
		self.down = [pygame.K_DOWN, pygame.K_s]
		self.left = [pygame.K_LEFT, pygame.K_a] # TODO: left and right functions
		self.right = [pygame.K_RIGHT, pygame.K_d]
		self.targetA = view.A
		self.fshowcompass = 0

	def think(self, dt, kpressed, kdowns):
		if any([up in kdowns for up in self.up]):
			self.moveup()
		elif any([down in kdowns for down in self.down]):
			self.movedown()
		elif any([left in kdowns for left in self.left]):
			self.movehoriz(1)
		elif any([right in kdowns for right in self.right]):
			self.movehoriz(-1)
		if pygame.K_q in kdowns:
			self.claimquest()

		# Smooth transition between stations
		self.ftarget += dt
		f = 100 * self.ftarget ** 3
		newyG0 = math.softapproach(view.yG0, self.targetyG0, f * dt, dymin = 0.01)
		# TODO: This is supposed to give a sense of pulling back every time you take a step, but I'm
		# not sure it comes across. Try it again once the graphics are more in place.
		# view.zoom = 100 / (1 + 0.001 * abs(view.yG0 - newyG0) / dt)
		view.yG0 = newyG0
		if view.yG0 == self.targetyG0:
			self.ftarget = 0

		view.A = view.Aapproach(view.A, self.targetA, 10 * dt)
		if self.fshowcompass > 0:
			self.fshowcompass = math.approach(self.fshowcompass, 0, 5 * dt)
		if view.dA(view.A, self.targetA):
			self.fshowcompass = 3

		quest.think(dt)
		dialog.think(dt)

	def moveup(self):
		aboves = [station.yG for station in state.stations if station.yG > self.targetyG0]
		self.targetyG0 = min(aboves) if aboves else state.top
	def movedown(self):
		belows = [station.yG for station in state.stations if station.yG < self.targetyG0]
		self.targetyG0 = max(belows) if belows else 0
	def movehoriz(self, dA):
		self.targetA = (round(self.targetA * 8) + dA) % 8 / 8
	def availablequest(self):
		s = state.currentstation()
		return s.quests[0] if s and s.quests else None
	def claimquest(self):
		q = self.availablequest()
		if q is not None:
			quest.start(q)
			state.currentstation().quests.pop(0)

	def draw(self):
		draw.stars()
		draw.atmosphere()
		for station in state.stations:
			station.draw(back = True)
		draw.cable()
		for station in state.stations:
			station.draw(back = False)
		worldmap.draw()
		text = "\n".join([
			"Station: %s" % (state.currentstationname(),),
			"Altitude: %d km" % (round(view.yG0),),
		])
		ptext.draw(text, fontsize = T(32), bottomleft = T(200, 720), owidth = 1.5)
		# Draw the compass
		alpha0 = math.clamp(self.fshowcompass, 0, 1)
		x0, y0 = 900, -30  # compass rose center
		for jA, dname in enumerate("N NE E SE S SW W NW".split()):
			A = view.dA(jA / 8, view.A)
			alpha = 1 if A == -0.5 else alpha0
			if alpha == 0:
				continue
			dy, dx = math.CS(A * math.tau, 100)
			pos = x0 + dx, y0 - dy
			ptext.draw(dname, center = T(pos), fontsize = T(60), owidth = 1.5,
				angle = -A * 360 + 180, alpha = alpha)
		if self.availablequest():
			ptext.draw("Quest available at this station! Press Q to begin.",
				center = pview.center, fontsize = T(80), width = T(720), color = "orange",
				owidth = 1.5)
		dialog.draw()
