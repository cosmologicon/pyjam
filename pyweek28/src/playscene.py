from __future__ import division
import pygame, math, random
from . import scene, pview, view, ptext, draw, state, worldmap, things, dialog, quest, hud, sound
from .pview import T


class PlayScene(scene.Scene):
	def __init__(self):
		state.stations = [
			things.Station("Ground Control", 0, 1000000),
#			things.Station("LowOrbiton", 700, 5),
			things.Station("Skyburg", 2000, 2),
#			things.Station("Last Ditch", 3700, 5),
#			things.Station("Stationary", 7200, 2),
			things.Station("Counterweight", 10000, 2),
		]
		for name in ["worker", "sci", "tech"]:
			p = things.Pop(name, state.stations[0])
		view.seek_z(state.stations[0].z)
		state.updatemissions()
		quest.start(quest.TutorialQuest())

		state.cars = [
			things.Car(0, j) for j in [0, 3]
		]
		self.hud = hud.HUD()
		self.hud.buttons.append(hud.Button("Rotate Left", (340, 360)))
		self.hud.buttons.append(hud.Button("Rotate Right", (940, 360)))
#		self.hud.buttons.append(hud.Button("Claim Quest", (640, 600), size = (160, 160), isvisible = self.availablequest))
		self.hud.buttons.append(hud.Button("Open/close Port", (880, 600), size = (160, 160), isvisible = state.currentstation))
		self.hud.buttons.append(hud.Button("Complete mission", (100, 600), size = (160, 40), isvisible = self.cancomplete))

		self.up = [pygame.K_UP, pygame.K_w]
		self.down = [pygame.K_DOWN, pygame.K_s]
		self.left = [pygame.K_LEFT, pygame.K_a]
		self.right = [pygame.K_RIGHT, pygame.K_d]
		self.fshowcompass = 0
		sound.playmusic('prologue')

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
		if pygame.K_b in kdowns:
			self.toggleblock()
		if pygame.K_1 in kdowns:
			self.adjustassignment(-1)
		if pygame.K_2 in kdowns:
			self.adjustassignment(1)
		if mdown:
			self.handlemousedown()

		if self.fshowcompass > 0:
			self.fshowcompass = math.approach(self.fshowcompass, 0, 5 * dt)
		if view.dA(view.A, view.targetA):
			self.fshowcompass = 3

		for obj in state.stations + state.cars:
			obj.think(dt)
			for passenger in obj.held:
				passenger.think(dt)

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
	def toggleblock(self):
		station = state.currentstation()
		if not station: return
		if view.A in range(8):
			station.toggleblock(view.A)
	def canfix(self):
		car = state.carat(view.zW0, view.A, dz = 3)
		return car and car.broken
	def cancomplete(self):
		s = state.currentstation()
		return s and s.mission and s.mission.fulfilled()
	def handlemousedown(self):
		if self.canfix():
			car = state.carat(view.zW0, view.A, dz = 3)
			screenpos = view.worldtoview(car.worldpos())
			d = T(20 + 1.2 * view.zoom)
			if math.distance(screenpos, self.mpos) < d:
				car.tryfix()
				return
		button = self.hud.buttonat(self.mpos)
		if button is not None:
			self.clickbutton(button.text)
			return
		car = worldmap.carat(self.mpos)
		if car is not None:
			view.seek_car(car)
			view.rotateto(car.A)
			return
		station = worldmap.stationat(self.mpos)
		if station is not None:
			view.seek_z(station.z)
			return
		station = state.currentstation()
		if station is not None:
			for rect, held in zip(cardrects(len(station.held)), station.held):
				if rect.collidepoint(self.mpos):
					scene.push(AssignScene(self, held))
					return
	def clickbutton(self, btext):
		if btext == "Rotate Left":
			sound.playsound("yes")
			view.rotate(1)
		elif btext == "Rotate Right":
			sound.playsound("yes")
			view.rotate(-1)
		elif btext == "Claim Quest":
			sound.playsound("yes")
			self.claimquest()
		elif btext == "Open/close Port":
			self.toggleblock()
		elif btext == "Complete mission":
			s = state.currentstation()
			if s and s.mission and s.mission.fulfilled():
				sound.playsound("yes")
				s.mission.finish()

	def draw(self):
		self.drawworld()
		worldmap.draw(worldmap.stationat(self.mpos), worldmap.carat(self.mpos))
		self.drawstationinfo()
		self.drawcarinfo()
		text = "\n".join([
			"Station: %s" % (state.currentstationname(),),
			"Altitude: %d km" % (round(view.zW0),),
		])
#		ptext.draw(text, fontsize = T(32), bottomleft = T(200, 720), owidth = 1.5)
		self.drawcompass()
		self.hud.draw()
		dialog.draw()

	def drawworld(self):
		draw.stars()
		draw.atmosphere()
		self.drawstate()
		draw.ground()

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
		coms.extend([(1.001, draw.portlights, [station]) for station in state.stations])
		for car in state.cars:
			if car.broken:
				pW = car.worldpos()
				pG, depth = view.worldtogame(pW)
				coms.append((depth + 0.6, draw.sparks, [pW]))
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
		text = info or ""
		ptext.draw(text, topleft = T(10, 70), fontsize = T(22), width = T(400), owidth = 1)

		text = "\n".join([
			"Current population: %d / %s" % (len(station.held), (station.capacity if station.capacity < 100000 else "unlimited")),
			"Port capacity: %d / 8" % station.portcapacity(),
		])
		ptext.draw(text, bottomleft = T(10, 360), fontsize = T(22), width = T(400), owidth = 1)
		for j, rect in enumerate(cardrects(station.showncapacity())):
			if j < len(station.held):
				station.held[j].drawcard(rect.center, rect.w)
			elif j < len(station.held) + len(station.pending):
				station.pending[j - len(station.held)].drawcard(rect.center, rect.w, alpha = 80)
			else:
				color = 10, 10, 10
				pview.screen.fill(color, rect)
				color = math.imix(color, (0, 0, 0), 0.5)
				pview.screen.fill(color, rect.inflate(T(-2), T(-2)))
		if station.mission:
			ptext.draw("Current mission: %s" % " ".join(station.mission.need), topleft = T(10, 600), fontsize = T(22), owidth = 1)

	def drawcarinfo(self):
		if state.currentstation():
			return
		car = state.currentcar()
		if car is None: return
		ptext.draw("Carrying:", topleft = T(20, 320), fontsize = T(26), owidth = 1)
		dest = state.stationat(car.targetz)
		for rect, held in zip(cardrects(len(car.held)), car.held):
			held.drawcard(rect.center, rect.w)
		if dest:
			ptext.draw("Destination: %s" % dest.name, topleft = T(20, 460), fontsize = T(26), owidth = 1)

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
			ptext.draw(dname, center = T(pos), fontsize = T(60), owidth = 1.5 if A == 0 else 0,
				angle = -A * 360 / 8, alpha = alpha)

def cardrects(n):
	for j in range(n):
		jy, jx = divmod(j, 10)
		size = T(72)
		pos = T(40 + 80 * jx, 400 + 80 * jy)
		rect = pygame.Rect(0, 0, size, size)
		rect.center = pos
		yield rect




# TODO: some other module about game mechanics.
stationinfo = {
	"Ground Control": "The surface of ALIENWORLD. Unlimited capacity. You can assign as many people here as you want.",
	"LowOrbiton": "Many spacecraft orbit at this level. You can trade goods here (not implemented yet).",
	"Skyburg": "The slightly reduced gravity at this level is ideal for training. You can assign workers new roles here (not implemented yet).",
	"Last Ditch": "The main communications array. If you upgrade the antenna enough, you might just hear something new.... (not implemented yet)",
	"Stationary": "The level of stationary orbit. Zero gravity.",
	"Counterweight": "Centrifugal force pulls you outward here. Ideal for launching deep-space vessels.",
}


class AssignScene(scene.Scene):
	def __init__(self, parent, held):
		self.parent = parent
		self.held = held
		self.t = 0
		sound.playsound("rising")

	def think(self, dt, kpressed, kdowns, mpos, mdown, mup):
		self.mpos = mpos
		self.t += dt
		if (self.t > 0.2 and mdown) or (self.t > 0.4 and mup):
			station = worldmap.stationat(self.mpos)
			if station and station.canaddpassenger():
				self.held.settargetholder(station)
			scene.pop()
			sound.playsound("dropping")

	def draw(self):
		self.parent.drawworld()
		alpha = int(math.clamp(500 * self.t, 0, 200))
		pview.fill((0, 0, 0, alpha))
		alpha = int(math.clamp(500 * self.t - 200, 0, 255))
		if alpha:
			ptext.draw("Drag the character to a station on the right to reassign.",
				center = pview.center, fontsize = T(50), shadow = (1, 1), width = T(500))

		worldmap.draw(worldmap.stationat(self.mpos), None)
		self.held.drawcard(self.mpos, T(80), alpha = 100)
