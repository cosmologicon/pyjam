import pygame, math
from . import scene, pview, view, ptext, draw, state, worldmap
from .pview import T

class PlayScene(scene.Scene):
	def __init__(self):
		# Where the camera wants to be.
		self.targetyG0 = 0
		self.ftarget = 0
		self.up = [pygame.K_UP, pygame.K_w]
		self.down = [pygame.K_DOWN, pygame.K_s]
		self.left = [pygame.K_LEFT, pygame.K_a] # TODO: left and right functions
		self.right = [pygame.K_RIGHT, pygame.K_d]
		self.stations = [station.Station(yG) for yG in state.stations]

	def think(self, dt, kpressed, kdowns):
		if any([up in kdowns for up in self.up]):
			self.moveup()
		elif any([down in kdowns for down in self.down]):
			self.movedown()

		# Smooth transition between stations
		self.ftarget += dt
		f = 100 * self.ftarget ** 3
		view.yG0 = math.softapproach(view.yG0, self.targetyG0, f * dt, dymin = 0.01)
		if view.yG0 == self.targetyG0:
			self.ftarget = 0

	def moveup(self):
		aboves = [station for station in state.stations if station > self.targetyG0]
		self.targetyG0 = min(aboves) if aboves else state.top
	def movedown(self):
		belows = [station for station in state.stations if station < self.targetyG0]
		self.targetyG0 = max(belows) if belows else 0


	def draw(self):
		# TODO: draw stars
		color = pview.I(math.fadebetween(view.yG0, 10, (100, 130, 220), 100, (0, 0, 0)))
		pview.fill(color)
		draw.cable()
		for stationyG in state.stations:
			draw.station(stationyG)
		worldmap.draw()
		text = "\n".join([
			"Altitude: %d km" % (round(view.yG0),),
		])
		ptext.draw(text, fontsize = T(32), bottomleft = T(200, 720), owidth = 1.5)
