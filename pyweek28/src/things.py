# Game entities

from __future__ import division
import pygame, random, math
from . import pview, view, quest, state, draw, ptext
from .pview import T

class Station:
	def __init__(self, name, z, pop = 0, capacity = 5):
		self.name = name
		self.capacity = capacity
		self.population = pop
		# "Shadow population", the population of the station once all cars complete their current
		# assingment.
		self.spopulation = self.population
		# Target population the player has set.
		self.assigned = self.population
		self.z = z
		self.messages = []
		self.quests = []
		self.t = 0
	def addquest(self, questname):
		self.quests.append(questname)
	def startquest(self, questname):
		self.quests.remove(questname)
		quest.start(questname)
	def think(self, dt):
		self.t += dt
	def draw(self):
		if not view.visible(self.z, 10):
			return
		dA = 0.1 * self.t
		draw.drawelement("gray", 0, self.z - 2, self.z - 0.7, 2, 4.2, 8, view.A, 10)
		draw.drawelement("hatch", 0, self.z - 0.7, self.z - 0.5, 4.2, 4.2, 1, view.A - 0 * dA, 100)
		draw.drawelement("window", 0, self.z - 0.5, self.z + 0.5, 4, 4, 1, view.A + dA, 20)
		draw.drawelement("hatch", 0, self.z + 0.5, self.z + 0.7, 4.2, 4.2, 1, view.A - 0 * dA, 100)
		draw.drawelement("gray", 0, self.z + 0.7, self.z + 1.4, 4.2, 2, 8, view.A, 10)

class Car:
	def __init__(self, z, A):
		self.z = z
		self.A = A
		self.n = 0  # number of passengers carried
		self.shadown = 0
		self.capacity = 1
		self.targetz = self.z
		self.vz = 0
		self.r = 0.8
		self.R = 1.3  # Distance from central axis
		# When a car nears its destination it switches to approach mode, which is exponential braking.
		self.braking = True
	def arrived(self):
		return self.targetz == self.z
	def worldpos(self):
		yW, xW = math.CS(self.A/8 * math.tau, self.R)
		return xW, yW, self.z
	def think(self, dt):
		if not self.arrived():
			b = 4  # braking factor. Set higher for shorter stops.
			brakez = math.softapproach(self.z, self.targetz, b * dt, dymin = 0.01)
			if not self.braking:
				self.vz += 200 * dt
				goz = math.approach(self.z, self.targetz, self.vz * dt)
				if abs(self.z - brakez) < abs(self.z - goz):
					self.braking = True
				else:
					self.z = goz
			if self.braking:
				self.vz = abs(brakez - self.z) / dt
				self.z = brakez
		if self.arrived():
			self.swappassengers()
			self.findtarget()
	def swappassengers(self):
		# Check whether we're at a station that has or needs passengers.
		# TODO: slight delay when accepting multiple passengers, like in Mini Metro.
		station = state.stationat(self.z)
		if not station:
			return
		dpop = station.population - station.assigned
		if dpop > 0 and self.capacity > self.n:
			dpop = min(dpop, self.capacity - self.n)
			self.n += dpop
			station.population -= dpop
			if station.spopulation != station.population:
				dspop = station.population - station.spopulation
				self.shadown -= dspop
				station.spopulation += dspop
		elif dpop < 0 and self.n > 0:
			dpop = min(-dpop, self.n)
			self.n -= dpop
			station.population += dpop
			if station.spopulation != station.population:
				dspop = station.population - station.spopulation
				self.shadown -= dspop
				station.spopulation += dspop
	def findtarget(self):
		# TODO: if there are multiple cars free in the same frame, assign the nearest one.
		if self.n > 0:
			# Find the nearest station that wants passengers.
			stations = [station for station in state.stations if station.assigned > station.spopulation]
			if stations:
				station = min(stations, key = lambda s: abs(self.z - s.z))
				self.settarget(station.z)
				togive = min(self.n, station.assigned - station.spopulation)
				station.spopulation += togive
				self.shadown -= togive
		elif self.n == 0:
			# Find the nearest station with extra passengers.
			stations = [station for station in state.stations if station.assigned < station.spopulation]
			if stations:
				station = min(stations, key = lambda s: abs(self.z - s.z))
				self.settarget(station.z)
				totake = min(self.capacity - self.n, station.spopulation - station.assigned)
				station.spopulation -= totake
				self.shadown += totake

	def settarget(self, zW):
		self.targetz = zW
		self.braking = False
	def draw(self, back):
		if not view.visible(self.z, 10):
			return
		(xG, yG), dG = view.worldtogame(self.worldpos())
		if (back and dG > 0) or (not back and dG < 0):
			return
		h = 0.5
		color = 200, 100, 100
		xV0, yV0 = view.gametoview((xG - self.r, yG + h))
		xV1, yV1 = view.gametoview((xG + self.r, yG - h))
		rect = pygame.Rect(xV0, yV0, xV1 - xV0, yV1 - yV0)
		if pview.rect.colliderect(rect):
			pview.screen.fill(color, rect)
			ptext.draw("%d/%d" % (self.n, self.capacity), center = view.gametoview((xG, yG)),
				fontsize = T(1 * view.zoom), owidth = 1, color = "orange")

