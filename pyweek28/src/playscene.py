import pygame, math
from . import scene, pview, view, ptext, draw, state
from .pview import T

class PlayScene(scene.Scene):
	def __init__(self):
		# Where the camera wants to be.
		self.targetyG0 = 0
	def think(self, dt, kpressed, kdowns):
		# TODO: support WASD
		if pygame.K_UP in kdowns:
			self.moveup()
		elif pygame.K_DOWN in kdowns:
			self.movedown()
		view.yG0 = math.softapproach(view.yG0, self.targetyG0, 10 * dt, dymin = 0.01)

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
		text = "\n".join([
			"Altitude: %d km" % (round(view.yG0),),
		])
		ptext.draw(text, fontsize = T(32), bottomleft = T(200, 720), owidth = 1.5)
