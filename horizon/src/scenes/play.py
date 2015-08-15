from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog, sound, image, ptext
from src.window import F


control = {}

def init():
	quest.quests["Act1"].available = True
	state.shipyard = {
		"Skiff": 600,
		"Mapper": 600,
		"Beacon": 600,
	}

	state.you = thing.Skiff(X = 0, y = state.R - 5, vx = 1)
	state.ships = [state.you]
	state.mother = thing.Mother(X = 0, y = state.R + 8)
	state.objs = [state.mother]
#	state.filaments = [thing.Filament(ladderps = state.worlddata["filaments"][0])]
	state.hazards = []
	for _ in range(500):
		X = random.uniform(0, math.tau)
		y = math.sqrt(random.uniform(state.Rcore ** 2, state.R ** 2))
		state.hazards.append(thing.Slash(X = X, y = y))
	for filament in state.worlddata["filaments"]:
		for j in range(len(filament) - 1):
			X0, y0 = filament[j]
			X1, y1 = filament[j+1]
			dX, dy = X1 - X0, y1 - y0
			state.hazards.append(thing.Rung(X = X0, y = y0))
			state.hazards.append(thing.Rung(X = X0 + dX / 3, y = y0 + dy / 3))
			state.hazards.append(thing.Rung(X = X0 + dX * 2 / 3, y = y0 + dy * 2 / 3))

	window.camera.follow(state.you)
	window.camera.think(0)

	populatefull()
	
	sound.playgamemusic()

def clearfull():
	state.ships = [ship for ship in state.ships if ship is state.you or ship.significant]

def populatefull():
	for shiptype, number in state.shipyard.items():
		shiptype = getattr(thing, shiptype)
		for _ in range(number):
			X = random.uniform(0, math.tau)
			y = math.sqrt(random.random()) * state.R
			if not state.Rcore + 1 < y < state.R - 1:
				continue
			state.ships.append(shiptype(X = X, y = y, vx = random.uniform(-6, 6)))

def repopulateslice():
	cam = window.camera
	fraction = (cam.Cy1 ** 2 - cam.Cy0 ** 2) / state.R ** 2 * cam.CdX * 2 / math.tau
	for shiptype, number in state.shipyard.items():
		shiptype = getattr(thing, shiptype)
		for _ in range(int(number * fraction)):
			X = random.uniform(-1, 1) * cam.CdX + cam.X0
			y = math.sqrt(random.uniform(cam.Cy0 ** 2, cam.Cy1 ** 2))
			if not state.Rcore + 1 < y < state.R - 1:
				continue
			ship = shiptype(X = X, y = y, vx = random.uniform(-6, 6))
			if window.camera.on(ship):
				thing.kill(ship)
				continue
			else:
				ship.vy = ship.targetvy()
				state.ships.append(ship)
	

def think(dt, events, kpressed):
	global todraw
	kx = kpressed["right"] - kpressed["left"]
	ky = kpressed["up"] - kpressed["down"]

	dt0 = dt
	if kpressed["go"] and control:
		dt *= 0.3

	hud.think(dt0)
	quest.think(dt)
	dialog.think(dt0)
	background.think(dt)
	sound.epicness = 2 - (state.you.y - 100) / 160
	sound.think(dt)

	oldX, oldy = state.you.X, state.you.y

	if 1e10 * random.random() < dt:
		state.ships.append(thing.Skiff(
			X = random.uniform(0, math.tau),
			y = state.R,
			vx = random.uniform(-6, 6)
		))
		state.ships.append(thing.Beacon(
			X = random.uniform(0, math.tau),
			y = state.R,
			vx = random.uniform(-6, 6)
		))
	nbubble = int(dt * 30) + (random.random() < dt * 30 % 1)
	for _ in range(nbubble):
		X = random.gauss(state.you.X, 30 / state.you.y)
		y = random.gauss(state.you.y, 30)
		if y < state.R - 10:
			state.effects.append(thing.Bubble(X = X, y = y))

	if sum(isinstance(effect, thing.BubbleChain) for effect in state.effects) < 10:
		for c in state.convergences:
			N = math.clamp((100 / window.distance(state.you, c)) ** 2, 0.05, 1)
			nbubble = int(dt * N) + (random.random() < dt * N % 1)
			for _ in range(nbubble):
				X = random.gauss(state.you.X, 30 / state.you.y)
				y = random.gauss(state.you.y, 30)
				if state.Rcore < y < state.R - 20:
					state.effects.append(thing.BubbleChain(X = X, y = y, X0 = c.X, y0 = c.y))


	for event in events:
		if event.type == KEYDOWN and event.key == "go":
			control.clear()
			control["cursor"] = state.you
			control["queue"] = {}
			control["qtarget"] = [state.you.X, state.you.y]
			control["t0"] = 0.001 * pygame.time.get_ticks()
		if event.type == KEYDOWN and event.key == "abort":
			if not state.you.significant:
				state.you.die()
			regenerate()
		if event.type == KEYUP:
			if not state.quickteleport and "queue" in control and event.key in ("up", "left", "right", "down"):
				control["queue"][event.key] = 0
		if event.type == KEYUP and event.key == "go" and "cursor" in control:
			if control["cursor"] is not state.you:
				state.effects.append(
					thing.Teleport(X = state.you.X, y = state.you.y, targetid = control["cursor"].thingid)
				)
				sound.play("teleport")
				state.you = control["cursor"]
			elif 0.001 * pygame.time.get_ticks() - control["t0"] < settings.tactivate:
				state.you.deploy()
			control.clear()
		
	if kpressed["go"] and control:
		if any(kpressed[x] for x in ("left", "right", "up", "down")):
			control["t0"] = -1000
		if state.quickteleport:
			control["qtarget"][0] += kx * dt0 * settings.vqteleport / control["qtarget"][1]
			control["qtarget"][1] += ky * dt0 * settings.vqteleport
			dx = math.Xmod(control["qtarget"][0] - state.you.X) * state.you.y
			dy = control["qtarget"][1] - state.you.y
			f = math.sqrt(dx ** 2 + dy ** 2) / settings.rqteleport
			if f > 1:
				dx /= f
				dy /= f
				control["qtarget"] = [state.you.X + dx / state.you.y, state.you.y + dy]
			retarget()
		else:
			q = control["queue"]
			for key in q:
				q[key] += dt0
				if q[key] >= settings.jumpcombotime:
					dx = ("right" in q) - ("left" in q)
					dy = ("up" in q) - ("down" in q)
					jump(dx, dy)
					q.clear()
					break
	else:
		dvx = kx * dt * 20
		dvy = ky * dt * 20
		state.you.vx += dvx
		state.you.vy = min(state.you.vy + dvy, 0)

	todraw = []
	scollide = []
	hcollide = []

	state.you.think(0)  # Clear out any controls that should be overridden

	for convergence in state.convergences:
		if window.camera.near(convergence):
			convergence.think(dt)
			todraw.append(convergence)


	repopulating = (dt + state.you.t % 1) // 1
	if repopulating:
		nships = []
		for ship in state.ships:
			if not window.camera.on(ship) and ship is not state.you and not ship.significant:
				continue
			ship.think(dt)
			if ship.alive:
				nships.append(ship)
				todraw.append(ship)
			else:
				ship.die()
		state.ships = nships
		repopulateslice()
	else:
		nships = []
		for ship in state.ships:
			if not window.camera.near(ship):
				nships.append(ship)
				continue
			ship.think(dt)
			if ship.alive:
				nships.append(ship)
				if window.camera.on(ship):
					todraw.append(ship)
			else:
				ship.die()
		state.ships = nships
	if not state.you.alive:
		regenerate()
	nobjs = []
	for obj in state.objs:
		if not window.camera.on(obj):
			nobjs.append(obj)
			continue
		obj.think(dt)
		if obj.alive:
			nobjs.append(obj)
			todraw.append(obj)
		else:
			obj.die()
	state.obj = nobjs
	for hazard in state.hazards:
		if not window.camera.near(hazard):
			continue
		hazard.think(dt)
		todraw.append(hazard)
		if window.camera.on(hazard):
			hcollide.append(hazard)
	state.obj = nobjs
#	for filament in state.filaments:
#		filament.think(dt)

	neffects = []
	for effect in state.effects:
		effect.think(dt)
		if effect.alive:
			todraw.append(effect)
			neffects.append(effect)
		else:
			effect.die()
	state.effects = neffects

	scollide = [state.you]
	for s in scollide:
		if not s.vulnerable():
			continue
		for h in hcollide:
			if window.distance(h, s) < h.hazardsize:
				s.takedamage(h.dhp)

	if window.dbycoord((oldX, oldy), (state.you.X, state.you.y)) > settings.rqteleport + 10:
		clearfull()
		populatefull()

	if state.quickteleport and "qtarget" in control:
		X, y = control["qtarget"]
		dX = math.Xmod(X - state.you.X)
		dy = y - state.you.y
		window.camera.X0 = state.you.X + dX * 0.5
		window.camera.y0 = state.you.y + dy * 0.5
		window.camera.setlimits()
	else:
		window.camera.follow(state.you)
		window.camera.think(dt)

def regenerate():
	state.you = thing.Skiff(X = state.mother.X, y = state.mother.y - 11, vx = 0)
	window.camera.X0 = state.you.X
	window.camera.y0 = state.you.y
	state.ships.append(state.you)
	clearfull()
	populatefull()
	sound.play("longteleport")
	control.clear()
	dialog.play("convo5")
	background.wash()
	background.drawwash()
	if settings.saveonemergency:
		state.save()


def jump(kx, ky):
	target = None
	d2 = settings.maxjump ** 2
	for ship in state.ships:
		if ship is control["cursor"]:
			continue
		dx = math.Xmod(ship.X - control["cursor"].X) * control["cursor"].y
		dy = ship.y - control["cursor"].y
		if dx * dx + dy * dy < d2:
			if abs(math.Xmod(math.atan2(kx, ky) - math.atan2(dx, dy))) < math.tau / 11:
				target = ship
				d2 = dx * dx + dy * dy
	if target:
		control["cursor"] = target

def retarget():
	target = None
	d2 = 4 * settings.rqteleport ** 2
	X, y = control["qtarget"]
	for ship in state.ships:
		if window.distance(ship, state.you) > settings.rqteleport:
			continue
		dx = math.Xmod(ship.X - X) * (ship.y + y) / 2
		dy = ship.y - y
		if dx ** 2 + dy ** 2 < d2:
			target = ship
			d2 = dx ** 2 + dy ** 2
	if target:
		control["cursor"] = target


def draw():
	if settings.drawbackground:
		background.draw()
	else:
		window.screen.fill((0, 60, 0))
	for obj in todraw:
		obj.draw()

	if "cursor" in control:
		image.worlddraw("cursor", control["cursor"].X, control["cursor"].y, 1.6,
			angle = pygame.time.get_ticks() * 0.15)
	if "qtarget" in control:
		X, y = control["qtarget"]
		image.worlddraw("qtarget", X, y, 1,
			angle = -pygame.time.get_ticks() * 0.15)
	dialog.draw()
	hud.draw()
	hud.drawstats()
	state.you.drawhud()
	dy = state.you.y - state.Rcore
	if dy < 36:
		alpha = pygame.time.get_ticks() * 0.001 % 1
		ptext.draw("Warning: Approaching data horizon", midtop = F(854/2, 100), color = "#FF7777",
			owidth = 1, fontsize = F(36), fontname = "NovaSquare", alpha = alpha)
	background.drawwash()


