from __future__ import division
import pygame, math
from . import scene, pview, view, ptext, draw, state, worldmap
from .pview import T

class PlayScene(scene.Scene):
	def __init__(self):
		# Where the camera wants to be.
		self.targetyG0 = view.yG0
		self.ftarget = 0
		self.targetA = view.A
		self.fshowcompass = 0

	def think(self, dt, kpressed, kdowns):
		# TODO: support WASD
		if pygame.K_UP in kdowns:
			self.moveup()
		elif pygame.K_DOWN in kdowns:
			self.movedown()
		elif pygame.K_LEFT in kdowns:
			self.movehoriz(1)
		elif pygame.K_RIGHT in kdowns:
			self.movehoriz(-1)

		# Smooth transition between stations
		self.ftarget += dt
		f = 100 * self.ftarget ** 3
		view.yG0 = math.softapproach(view.yG0, self.targetyG0, f * dt, dymin = 0.01)
		if view.yG0 == self.targetyG0:
			self.ftarget = 0

		view.A = view.Aapproach(view.A, self.targetA, 10 * dt)
		if self.fshowcompass > 0:
			self.fshowcompass = math.approach(self.fshowcompass, 0, 5 * dt)
		if view.dA(view.A, self.targetA):
			self.fshowcompass = 3

	def moveup(self):
		aboves = [station for station in state.stations if station > self.targetyG0]
		self.targetyG0 = min(aboves) if aboves else state.top
	def movedown(self):
		belows = [station for station in state.stations if station < self.targetyG0]
		self.targetyG0 = max(belows) if belows else 0
	def movehoriz(self, dA):
		self.targetA = (round(self.targetA * 8) + dA) % 8 / 8

	def draw(self):
		draw.stars()
		draw.atmosphere()
		for stationyG in state.stations:
			draw.station(stationyG, back = True)
		draw.cable()
		for stationyG in state.stations:
			draw.station(stationyG, back = False)
		worldmap.draw()
		text = "\n".join([
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
				

