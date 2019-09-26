from __future__ import division
import pygame, math, random
from . import scene, pview, view, ptext, draw, state, worldmap, things, dialog, quest, hud
from .pview import T

class PlayScene(scene.Scene):
	def __init__(self):
		state.stations = [
			things.Station("LowOrbiton", 400),
			things.Station("Skyburg", 2000),
			things.Station("Last Ditch", 3700),
			things.Station("Stationary", 7200),
			things.Station("Counterweight", 10000, pop = 5),
		]
		#state.stations[3].addquest("testquest")
		state.stations[4].addquest("reallocate")
		
		state.cars = [
			things.Car(random.uniform(0, state.top), j) for j in range(8)
		]
		self.hud = hud.HUD()

		self.up = [pygame.K_UP, pygame.K_w]
		self.down = [pygame.K_DOWN, pygame.K_s]
		self.left = [pygame.K_LEFT, pygame.K_a]
		self.right = [pygame.K_RIGHT, pygame.K_d]
		self.fshowcompass = 0

	def think(self, dt, kpressed, kdowns, mpos, mdown, mup):
		self.mpos = mpos
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
		if pygame.K_1 in kdowns:
			self.adjustassignment(-1)
		if pygame.K_2 in kdowns:
			self.adjustassignment(1)
		self.handlemouse(mdown, mup)

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
	def adjustassignment(self, n):
		s = state.currentstation()
		if not s: return
		s.assigned = math.clamp(s.assigned + n, 0, s.capacity)
	def seekcar(self):
		carshere = [c for c in state.cars if view.dA(c.A, view.targetA) == 0]
		if not carshere:
			return
		view.seek_car(carshere[0])
	def getpointedstation(self):
		# TODO: a lot of repeated logic here with worldmap.draw.
		for station in state.stations:
			yV = pview.I(math.fadebetween(station.z, 0, T(660), state.top, T(60)))
			rect = T(pygame.Rect(0, 0, 150, 20))
			rect.center = T(1140), yV
			if rect.collidepoint(self.mpos):
				return station
		return None
	def handlemouse(self, mdown, mup):
		if mdown:
			button = self.hud.buttonat(self.mpos)
			if button is not None:
				self.clickbutton(button.text)
			station = self.getpointedstation()
			if station is not None:
				view.seek_z(station.z)
	def clickbutton(self, btext):
		if btext == "Rotate Left":
			view.rotate(-1)
		elif btext == "Rotate Right":
			view.rotate(1)


	def draw(self):
		draw.stars()
		draw.atmosphere()

		self.drawstate()
		worldmap.draw(self.getpointedstation())
		self.drawstationinfo()
		text = "\n".join([
			"Station: %s" % (state.currentstationname(),),
			"Altitude: %d km" % (round(view.zW0),),
		])
		ptext.draw(text, fontsize = T(32), bottomleft = T(200, 720), owidth = 1.5)
		self.drawcompass()
		self.hud.draw()
		if self.availablequest():
			ptext.draw("Quest available at this station! Press Q to begin.",
				center = pview.center, fontsize = T(80), width = T(720), color = "orange",
				owidth = 1.5)
		dialog.draw()

	# Draw game objects, and the cable.
	def drawstate(self):
		objs = state.cars + state.stations
		# espec fields are: texturename, xG, yG, zG0, zG1, 
		especs = [espec for obj in objs for espec in obj.especs()]
		def drawargs(espec):
			texturename, xW, yW, zW0, zW1, r0, r1, n, dA, k = espec
			(xG, yG0), depth = view.worldtogame((xW, yW, zW0))
			yG1 = yG0 + (zW1 - zW0)
			r = (r0 + r1) / 2
			sortkey = depth + 0.6 * r
			args = texturename, xG, yG0, yG1, r0, r1, n, view.A + dA, k
			return sortkey, draw.drawelement, args
		coms = [drawargs(espec) for espec in especs]
		coms.append((1, draw.cable, []))
		for _, func, args in sorted(coms, key = lambda com: com[0]):
			func(*args)


	# TODO: could go in a HUD module.
	def drawstationinfo(self):
		station = state.currentstation()
		if station is None:
			return
		ptext.draw("Welcome to", midtop = T(140, 6), fontsize = T(24), owidth = 1)
		ptext.draw(station.name, midtop = T(140, 26), fontsize = T(42), owidth = 1)
		info = stationinfo.get(station.name)
		if info is not None:
			ptext.draw(info, topleft = T(10, 70), fontsize = T(22), width = T(220), owidth = 1)
		text = "\n".join([
			"Current population: %d" % station.population,
			"Shadow population: %d" % station.spopulation,
			"Current assigment: %d" % station.assigned,
			"Total capacity: %d" % station.capacity,
		])
		ptext.draw(text, topleft = T(10, 260), fontsize = T(22), owidth = 1)



	# TODO: move to some other module
	def drawcompass(self):
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


# TODO: some other module about game mechanics.
stationinfo = {
	"LowOrbiton": "Many spacecraft orbit at this level. You can trade goods here (not implemented yet).",
	"Skyburg": "The slightly reduced gravity at this level is ideal for training. You can assign workers new roles here (not implemented yet).",
	"Last Ditch": "The main communications array. If you upgrade the antenna enough, you might just hear something new.... (not implemented yet)",
	"Stationary": "The level of stationary orbit. Zero gravity.",
	"Counterweight": "Centrifugal force pulls you outward here. Ideal for launching deep-space vessels.",
}

