from __future__ import division
import pygame, math, random
from . import scene, pview, view, ptext, draw, state, worldmap, things, dialog, quest
from .pview import T

class PlayScene(scene.Scene):
	def __init__(self):
		state.stations = [
			things.Station("LowOrbiton", 400),
			things.Station("Skyburg", 2000),
			things.Station("Last Ditch", 3700),
			things.Station("Stationary", 7200),
			things.Station("Counterweight", 10000),
		]
		state.stations[3].addquest("testquest")
		
		state.cars = [
			things.Car(random.uniform(0, state.top), j) for j in range(8)
		]

		self.up = [pygame.K_UP, pygame.K_w]
		self.down = [pygame.K_DOWN, pygame.K_s]
		self.left = [pygame.K_LEFT, pygame.K_a]
		self.right = [pygame.K_RIGHT, pygame.K_d]
		self.fshowcompass = 0

	def think(self, dt, kpressed, kdowns):
		if any([up in kdowns for up in self.up]):
			self.moveup()
		elif any([down in kdowns for down in self.down]):
			self.movedown()
		elif any([left in kdowns for left in self.left]):
			view.rotate(1)
		elif any([right in kdowns for right in self.right]):
			view.rotate(-1)
		if pygame.K_q in kdowns:
			self.claimquest()
		if pygame.K_c in kdowns:
			self.seekcar()

		if self.fshowcompass > 0:
			self.fshowcompass = math.approach(self.fshowcompass, 0, 5 * dt)
		if view.dA(view.A, view.targetA):
			self.fshowcompass = 3

		for obj in state.stations + state.cars:
			obj.think(dt)

		view.think(dt)
		quest.think(dt)
		dialog.think(dt)

	# TODO: not sure these do the right thing if you hit them twice in a row quickly.
	def moveup(self):
		targetz = view.targetz if view.cmode == "z" else view.zW0
		aboves = [station.z for station in state.stations if station.z > targetz]
		view.seek_z(min(aboves) if aboves else state.top)
	def movedown(self):
		targetz = view.targetz if view.cmode == "z" else view.zW0
		belows = [station.z for station in state.stations if station.z < targetz]
		view.seek_z(max(belows) if belows else 0)
	def availablequest(self):
		s = state.currentstation()
		return s.quests[0] if s and s.quests else None
	def claimquest(self):
		q = self.availablequest()
		if q is not None:
			quest.start(q)
			state.currentstation().quests.pop(0)
	def seekcar(self):
		carshere = [c for c in state.cars if view.dA(c.A, view.targetA) == 0]
		if not carshere:
			return
		view.seek_car(carshere[0])

	def draw(self):
		draw.stars()
		draw.atmosphere()

		# TODO: better for drawing all the world objects is to have each one have a set of pieces
		# which can then be sorted by depth.
		for car in state.cars:
			car.draw(back = True)
		draw.cable()
		for car in state.cars:
			car.draw(back = False)
		for station in state.stations:
			station.draw()
		worldmap.draw()
		text = "\n".join([
			"Station: %s" % (state.currentstationname(),),
			"Altitude: %d km" % (round(view.zW0),),
		])
		ptext.draw(text, fontsize = T(32), bottomleft = T(200, 720), owidth = 1.5)
		# Draw the compass
		alpha0 = math.clamp(self.fshowcompass, 0, 1)
		x0, y0 = 900, -30  # compass rose center
		for jA, dname in enumerate(view.Anames):
			A = view.dA(jA, view.A)
			alpha = 1 if A == 0 else alpha0
			if alpha == 0:
				continue
			# I'm like 90% sure this formula is wrong in at least one way but it works so whatever.
			dy, dx = math.CS(-(A + 4) / 8 * math.tau, 100)
			pos = x0 - dx, y0 - dy
			ptext.draw(dname, center = T(pos), fontsize = T(60), owidth = 1.5,
				angle = -A * 360 / 8, alpha = alpha)
		if self.availablequest():
			ptext.draw("Quest available at this station! Press Q to begin.",
				center = pview.center, fontsize = T(80), width = T(720), color = "orange",
				owidth = 1.5)
		dialog.draw()
