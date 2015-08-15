from __future__ import division
import math, random, pygame
from src import window, image, state, hud, sound, settings, background, dialog
from src.window import F
from src.enco import Component

things = {}
nextthingid = 1

def add(thing):
	things[thing.thingid] = thing
	return thing.thingid
def get(thingid):
	return things.get(thingid, None)
def kill(thing):
	if thing.thingid in things:
		del things[thing.thingid]
def newid():
	global nextthingid
	n = nextthingid
	nextthingid += 1
	return n

class HasId(Component):
	def init(self, thingid = None, **kwargs):
		self.thingid = newid() if thingid is None else thingid
	def dump(self, obj):
		obj["thingid"] = self.thingid
	def die(self):
		kill(self)

class HasType(Component):
	def dump(self, obj):
		obj["type"] = self.__class__.__name__

class KeepsTime(Component):
	def init(self, t = 0, **kwargs):
		self.t = t
	def think(self, dt):
		self.t += dt
	def dump(self, obj):
		obj["t"] = self.t

class Alive(Component):
	def init(self, alive = True, **kwargs):
		self.alive = alive
	def dump(self, obj):
		obj["alive"] = self.alive
	def die(self):
		self.alive = False

class HasHealth(Component):
	def __init__(self, maxhp):
		self.maxhp = maxhp
	def init(self, hp = None, tflash = 0, **kwargs):
		self.hp = self.maxhp if hp is None else hp
		self.tflash = tflash
	def dump(self, obj):
		obj["hp"] = self.hp
		obj["tflash"] = self.tflash
	def vulnerable(self):
		return self.tflash == 0
	def think(self, dt):
		self.tflash = max(self.tflash - dt, 0)
	def takedamage(self, dhp):
		if not self.vulnerable():
			return
		self.hp -= dhp
		if self is state.you:
			sound.play("ouch")
		self.tflash = settings.thurtinvulnerability
		if self.hp <= 0:
			self.die()

class Lifetime(Component):
	def __init__(self, lifetime = 1):
		self.lifetime = lifetime
		self.flife = 0
	def think(self, dt):
		if self.t > self.lifetime:
			self.alive = False
		self.flife = math.clamp(self.t / self.lifetime, 0, 1)

class WorldBound(Component):
	def init(self, X = None, y = None, pos = None, **kwargs):
		self.X = X or 0
		self.y = y or 0
		if pos is not None:
			self.X, self.y = pos
	def dump(self, obj):
		obj["X"] = self.X
		obj["y"] = self.y
	def screenpos(self):
		return window.screenpos(self.X, self.y)
	def think(self, dt):
		if self.y < 0:
			self.alive = False

class DiesAtCore(Component):
	def think(self, dt):
		if self.y <= state.Rcore:
			self.die()

class WinsAtCore(Component):
	def think(self, dt):
		from src import quest, scene
		if self.y <= state.Rcore and quest.quests["Finale"].done:
			from src.scenes import finalcutscene
			scene.current = finalcutscene
			scene.toinit = finalcutscene
			quest.quests["Finale"].winner = self.__class__.__name__

class HasVelocity(Component):
	def init(self, vx = 0, vy = 0, **kwargs):
		self.vx = vx
		self.vy = vy
	def dump(self, obj):
		obj["vx"] = self.vx
		obj["vy"] = self.vy
	def think(self, dt):
		self.X += self.vx * dt / self.y
		self.y += self.vy * dt
	def screenpos(self):
		return window.screenpos(self.X, self.y)

class Converges(Component):
	def __init__(self, v = 8):
		self.v = v
	def init(self, X0, y0, **kwargs):
		self.X0 = X0
		self.y0 = y0
	def dump(self, obj):
		obj["X0"] = self.X0
		obj["y0"] = self.y0
	def think(self, dt):
		dx = math.Xmod(self.X0 - self.X) * self.y
		dy = self.y0 - self.y
		d = math.sqrt(dx ** 2 + dy ** 2)
		if d < 2:
			self.die()
		else:
			f = min(dt * self.v / d, 1)
			self.X += dx * f / self.y
			self.y += dy * f

class Drifts(Component):
	def init(self, driftax = 0, **kwargs):
		self.driftax = driftax
	def dump(self, obj):
		obj["driftax"] = self.driftax
	def think(self, dt):
		if self is not state.you:
			self.driftax += dt * random.uniform(-0.3, 0.3)
			self.driftax = math.clamp(self.driftax, -0.5, 0.5)
			self.vx += dt * self.driftax

class DropsDown(Component):
	def __init__(self, dropay = 10):
		self.dropay = dropay
	def think(self, dt):
		self.vy -= self.dropay * dt

class FeelsLinearDrag(Component):
	def __init__(self, beta):
		self.beta = beta
	def think(self, dt):
		if self.vx or self.vy:
			f = math.exp(-self.beta * dt)
			self.vx *= f
			self.vy *= f

class HasMaximumHorizontalVelocity(Component):
	def __init__(self, vxmax):
		self.vxmax = vxmax
	def think(self, dt):
		self.vx = math.clamp(self.vx, -self.vxmax, self.vxmax)

class HasMaximumVerticalVelocity(Component):
	def __init__(self, vymax):
		self.vymax = vymax
	def think(self, dt):
		self.vy = math.clamp(self.vy, -self.vymax, self.vymax)

class VerticalWeight(Component):
	def targetvy(self):
		return -self.vymax * (2 * state.Rcore / self.y)
	def think(self, dt):
		if self is not state.you:
			self.vy += 0.2 * dt * (self.targetvy() - self.vy)

class MovesCircularWithConstantSpeed(Component):
	def __init__(self, speed, vomega):
		self.speed = speed
		self.vomega = vomega
	def init(self, vphi = None, **kwargs):
		self.vphi = random.uniform(0, math.tau) if vphi is None else vphi
	def dump(self, obj):
		obj["vphi"] = self.vphi
	def think(self, dt):
		self.vphi += self.vomega * dt
		self.vx = self.speed * math.sin(self.vphi)
		self.vy = self.speed * math.cos(self.vphi)

# Position appearing on screen is offset horizontally
class HorizontalOscillation(Component):
	def __init__(self, xA, xomega):
		self.xA = xA
		self.xomega = xomega
	def screenpos(self):
		dX = self.xA * math.sin(self.xomega * self.t) / self.y
		return window.screenpos(self.X + dX, self.y)

class DrawImage(Component):
	def __init__(self, imgname, imgr = settings.usershipsize):
		self.imgname = imgname
		self.imgr = imgr
	def draw(self):
		if self.y <= 0:
			return
		image.worlddraw(self.imgname, self.X, self.y, self.imgr, angle = -self.vx)

class DrawImageFlash(Component):
	def __init__(self, imgname, imgr = settings.usershipsize):
		self.imgname = imgname
		self.imgr = imgr
	def draw(self):
		if self.y <= 0:
			return
		if self.tflash:
			if self.tflash * 10 % 2 > 1:
				return
		image.worlddraw(self.imgname, self.X, self.y, self.imgr, angle = -self.vx)

class Hidden(Component):
	def __init__(self, rdetect = None):
		self.rdetect = rdetect or settings.beacondetect
	def init(self, tvisible = 0, **kwargs):
		self.tvisible = tvisible
	def dump(self, obj):
		obj["tvisible"] = self.tvisible
	def isvisible(self):
		for obj in state.beacons:
			if window.distance(obj, self) < self.rdetect:
				return True
		return False		
	def think(self, dt):
		if self.isvisible():
			self.tvisible += dt
		else:
			self.tvisible = 0

class DrawHiddenImage(Component):
	def __init__(self, imgname, imgr = 1):
		self.imgname = imgname
		self.imgr = imgr
	def draw(self):
		if self.y <= 0:
			return
		if not self.tvisible:
			return
		alpha = min(self.tvisible, 0.5 + 0.4 * math.sin(self.t))
		image.worlddraw(self.imgname, self.X, self.y, self.imgr, alpha = alpha)

class DrawHiddenRotatingImage(Component):
	def __init__(self, imgname, imgr = 1):
		self.imgname = imgname
		self.imgr = imgr
	def draw(self):
		if self.y <= 0:
			return
		if not self.tvisible:
			return
		alpha = min(self.tvisible, 0.5 + 0.4 * math.sin(self.t))
		image.worlddraw(self.imgname, self.X, self.y, self.imgr, alpha = alpha, angle = 200 * self.t)

class DrawTarget(Component):
	def draw(self):
		p = window.screenpos(self.X, self.y)
		color = tuple(int(a * (0.8 + 0.2 * math.sin(8 * self.t))) for a in (255, 128, 128))
		pygame.draw.circle(window.screen, color, p, F(5), 0)
		pygame.draw.circle(window.screen, color, p, F(10), F(1))
		pygame.draw.circle(window.screen, color, p, F(15), F(1))

class DrawTargetOverParent(Component):
	def init(self, parentid = None, **kwargs):
		self.parentid = parentid
	def dump(self, obj):
		obj["parentid"] = self.parentid
	def think(self, dt):
		if get(self.parentid) is state.you:
			self.alive = False
	def draw(self):
		parent = get(self.parentid)
		p = window.screenpos(parent.X, parent.y)
		color = tuple(int(a * (0.8 + 0.2 * math.sin(8 * self.t))) for a in (128, 255, 128))
		pygame.draw.circle(window.screen, color, p, F(5), 0)
		pygame.draw.circle(window.screen, color, p, F(10), F(1))
		pygame.draw.circle(window.screen, color, p, F(15), F(1))

class LeavesCorpse(Component):
	def die(self):
		corpse = Corpse(X = self.X, y = self.y, vx = self.vx, vy = self.vy,
			imgname = self.imgname, imgr = self.imgr)
		add(corpse)
		state.effects.append(corpse)

class DrawCorpse(Component):
	def init(self, imgname = None, imgr = None, imgomega = None, **kwargs):
		self.imgname = imgname
		self.imgr = imgr
		self.imgomega = random.uniform(4, 8) * random.choice([-1, 1]) if imgomega is None else imgomega
	def dump(self, obj):
		obj["imgname"] = self.imgname
		obj["imgr"] = self.imgr
		obj["imgomega"] = self.imgomega
	def draw(self):
		if self.y <= 0:
			return
		image.worlddraw(self.imgname, self.X, self.y, self.imgr, angle = self.imgomega * self.t,
			alpha = 1 - self.flife)

class DrawTremor(Component):
	def __init__(self):
		self.nimgs = 20
		self.timg = 1.5
	def init(self, imgs = None, **kwargs):
		self.imgs = imgs or []
	def dump(self, obj):
		obj["imgs"] = self.imgs
	def think(self, dt):
		while self.imgs and self.t - self.imgs[0][2] > self.timg:
			self.imgs.pop(0)
		while len(self.imgs) < self.nimgs:
			st = self.timg / 2
			X = random.gauss(self.X + self.vx * st / self.y, 2 / self.y)
			y = random.gauss(self.y + self.vy * st, 2)
			t = self.t - (self.nimgs - len(self.imgs) - 1) * self.timg / self.nimgs
			self.imgs.append((X, y, t))
	def draw(self):
		for X, y, t in self.imgs:
			t = (self.t - t) / self.timg
			if not 0 < t < 1:
				continue
			alpha = t * (1 - t)
			image.worlddraw("tremor", X, y, 6, rotate = False, alpha = alpha)

class DrawSlash(Component):
	def __init__(self):
		self.nimgs = 15
		self.timg = 2.5
	def init(self, imgs = None, **kwargs):
		self.imgs = imgs or []
	def dump(self, obj):
		obj["imgs"] = self.imgs
	def think(self, dt):
		while self.imgs and self.t - self.imgs[0][3] > self.timg:
			self.imgs.pop(0)
		while len(self.imgs) < self.nimgs:
			t0 = (self.nimgs - len(self.imgs) - 1) * self.timg / self.nimgs
			st = t0 + self.timg / 2
			X = random.gauss(self.X + self.vx * st / self.y, 2 / self.y)
			y = random.gauss(self.y + self.vy * st, 2)
			t = self.t - t0
			self.imgs.append((X, y, random.uniform(0, 360), t))
	def draw(self):
		for X, y, angle, t in self.imgs:
			if not state.Rcore + 5 < y < state.R - 5:
				continue
			t = (self.t - t) / self.timg
			if not 0 < t < 1:
				continue
			alpha = t * (1 - t)
			image.worlddraw("slash-red", X, y, 6, angle = angle, alpha = alpha)

class DrawRung(Component):
	def __init__(self):
		self.nimgs = 12
		self.timg = 2.5
	def init(self, imgs = None, **kwargs):
		self.imgs = imgs or []
	def dump(self, obj):
		obj["imgs"] = self.imgs
	def think(self, dt):
		while self.imgs and self.t - self.imgs[0][3] > self.timg:
			self.imgs.pop(0)
		while len(self.imgs) < self.nimgs:
			st = self.timg / 2
			X = random.gauss(self.X + self.vx * st / self.y, 3 / self.y)
			y = random.gauss(self.y + self.vy * st, 3)
			t = self.t - (self.nimgs - len(self.imgs) - 1) * self.timg / self.nimgs
			color = "red"
			self.imgs.append((X, y, random.uniform(0, 360), t, color))
	def draw(self):
		for X, y, angle, t, color in self.imgs:
			if not state.Rcore + 7 < y < state.R - 7:
				continue
			t = (self.t - t) / self.timg
			if not 0 < t < 1:
				continue
			alpha = t * (1 - t)
			image.worlddraw("slash-" + color, X, y, 6, angle = angle, alpha = alpha)

# Whether the object is important to the plot, and should not be discarded if it's offscreen.
class HasSignificance(Component):
	def init(self, significant = False, **kwargs):
		self.significant = significant
	def dump(self, obj):
		obj["significant"] = self.significant


class IgnoresNetwork(Component):
	def rnetwork(self):
		return 0

class CanDeploy(Component):
	def init(self, deployed = False, **kwargs):
		self.deployed = deployed
	def dump(self, obj):
		obj["deployed"] = self.deployed
	def deploy(self):
		self.deployed = not self.deployed
		self.significant = self.deployed
		sound.play("chirpup" if self.deployed else "chirpdown")

class CanDeployOnce(Component):
	def init(self, deployed = False, **kwargs):
		self.deployed = deployed
	def dump(self, obj):
		obj["deployed"] = self.deployed
	def deploy(self):
		if self.deployed:
			sound.play("no")
		else:
			self.deployed = True
			self.significant = True
			sound.play("chirpup")

class CantDeploy(Component):
	def deploy(self):
		sound.play("no")

class DeployFreeze(Component):
	def think(self, dt):
		if self.deployed:
			self.vx = self.vy = 0

class DeployComm(Component):
	def __init__(self, networkreach = 20):
		self.networkreach = networkreach
	def deploy(self):
		state.buildnetwork()
	def rnetwork(self):
		return self.networkreach if self.deployed else 0
	def draw(self):
		if self.deployed:
			dX = 3 * math.sin(4 * self.t) / self.y
			dy = 3 * math.cos(4 * self.t)
			px, py = window.screenpos(self.X + dX, self.y + dy)
			size = F(2)
			window.screen.fill((255, 255, 255), (px, py, size, size))

class BeaconDeploy(Component):
	def deploy(self):
		nvis0 = sum(obj.isvisible() for obj in state.goals + state.convergences)
		if self in state.beacons:
			state.beacons.remove(self)
		if self.deployed:
			state.beacons.append(self)
		nvis1 = sum(obj.isvisible() for obj in state.goals + state.convergences)
		if nvis1 > nvis0:
			sound.play("reveal")
	def think(self, dt):
		if self.deployed:
			self.hp = 1000
	def draw(self):
		if not self.deployed:
			return
		r = settings.beacondetect - 1
		for j in range(3):
			a = 4 * self.t + j * math.tau / 3
			X = self.X + r * math.sin(a) / self.y
			y = self.y + r * math.cos(a)
			pygame.draw.circle(window.screen, (200, 200, 50), window.screenpos(X, y), F(2))
	def die(self):
		if self in state.beacons:
			state.beacons.remove(self)


class DeployShield(Component):
	def deploy(self):
		if self in state.shields:
			state.shields.remove(self)
		if self.deployed:
			state.shields.append(self)
	def draw(self):
		if self.deployed:
			image.worlddraw("shield", self.X, self.y, settings.rshield, rotate = False,
				alpha = 0.6 + 0.4 * math.sin(self.t))

class Laddered(Component):
	def init(self, ladderps = None, **kwargs):
		self.ladderps = ladderps
		self.ladderds = []
		for j, (X, y) in enumerate(self.ladderps):
			X0, y0 = self.ladderps[max(j-1, 0)]
			X2, y2 = self.ladderps[min(j+1, len(self.ladderps)-1)]
			dx = (X2 - X0) * y
			dy = y2 - y0
			d = math.sqrt(dx ** 2 + dy ** 2)
			self.ladderds.append(((dy/d) / y, -(dx/d)))
	def dump(self, obj):
		obj["ladderps"] = self.ladderps

class DrawFilament(Component):
	def draw(self, surf, factor):
		data = []
		for j, ((X, y), (dX, dy)) in enumerate(zip(self.ladderps, self.ladderds)):
			if window.distancefromcamera(X, y) < 3:
				data.append((j, X, y, dX, dy))
		if len(data) < 2:
			return
		for alpha, r in [(40, 20), (60, 16), (100, 12), (140, 8)]:
			ps = []
			rps = []
			for j, X, y, dX, dy in data:
				omegax = 0.6 + 0.6 * (j ** 1.4 % 1)
				omegay = 0.6 + 0.6 * (j ** 1.7 % 1)
				omegar = 0.6 + 0.6 * (j ** 1.8 % 1)
				X += 4 * math.sin(omegax * self.t) / y
				y += 4 * math.sin(omegay * self.t)
				dr = r * (1 + 0.2 * math.sin(omegar * self.t))
				dX *= dr
				dy *= dr
				px, py = window.screenpos(X + dX, y + dy)
				ps.append((px / factor, py / factor))
				px, py = window.screenpos(X - dX, y - dy)
				rps.append((px / factor, py / factor))
			pygame.draw.polygon(surf, (255, 255, 0, alpha), ps + rps[::-1], 0)

class EmptyDrawHUD(Component):
	def drawhud(self):
		pass

class DrawMinimap(Component):
	def drawhud(self):
		hud.drawminimap()

class MapperDeploy(Component):
	def drawhud(self):
		if self.deployed:
			hud.drawmap()
		else:
			hud.drawminimap()

class WarpDeploy(Component):
	def deploy(self):
		sound.play("warp")
		self.X += math.tau / 1.618
		window.camera.X0 += math.tau / 1.618
		self.X %= math.tau
		window.camera.X0 %= math.tau
		self.tflash = settings.twarpinvulnerability
		state.effects.append(WarpEffect(X = self.X, y = self.y))

class DrawGoalArrows(Component):
	def draw(self):
		if not self.deployed:
			return
		px0, py0 = window.screenpos(self.X, self.y)
		for obj in state.goals:
			dx = math.Xmod(obj.X - self.X) * (self.y + obj.y) / 2
			dy = obj.y - self.y
			d = math.sqrt(dx ** 2 + dy ** 2)
			if d < 8:
				continue
			dx /= d
			dy /= d
			px = px0 + int(window.camera.R * 2 * dx)
			py = py0 - int(window.camera.R * 2 * dy)
			pygame.draw.circle(window.screen, (0, 0, 255), (px, py), F(2))

class DrawBubbles(Component):
	def init(self, bubble = None, **kwargs):
		self.bubble = bubble
	def think(self, dt):
		if self.bubble is None:
			X = random.gauss(self.X, 15 / self.y)
			y = random.gauss(self.y, 15)
			self.bubble = X, y, self.t
			if self.bubble[1] >= state.R:
				self.bubble = None
		if self.bubble and self.t - self.bubble[2] > 1:
			self.bubble = None
	def draw(self):
		if not self.bubble:
			return
		X, y, t = self.bubble
		t = self.t - t
		p = window.screenpos(X, y)
		r = max(F(6 * t), F(1))
		pygame.draw.circle(window.screen, (0, 60, 30), p, r, F(1))


class DrawConvergence(Component):
	def __init__(self):
		self.nimgs = 30
		self.timg = 2.5
	def init(self, imgs = None, **kwargs):
		self.imgs = imgs or []
	def dump(self, obj):
		obj["imgs"] = self.imgs
	def think(self, dt):
		while self.imgs and self.t - self.imgs[0][2] > self.timg:
			self.imgs.pop(0)
		while len(self.imgs) < self.nimgs:
			st = self.timg / 2
			r = random.uniform(0, 20)
			theta = random.uniform(0, math.tau)
			X = self.X + r * math.sin(theta) / self.y
			y = self.y + r * math.cos(theta)
			t = self.t - (self.nimgs - len(self.imgs) - 1) * self.timg / self.nimgs
			s = random.uniform(6, 12)
			color = random.choice(["white", "red", "yellow", "orange", "green", "blue", "purple"])
			self.imgs.append((X, y, t, s, "tremor-" + color))
	def draw(self):
		if not self.tvisible:
			return
		for X, y, t, s, iname in self.imgs:
			t = (self.t - t) / self.timg
			if not 0 < t < 1:
				continue
			alpha = min(self.tvisible, 2 * t * (1 - t))
			image.worlddraw(iname, X, y, s, rotate = False, alpha = alpha)

class DrawBlob(Component):
	def init(self, s = None, **kwargs):
		self.s = s or random.uniform(3, 6)
	def dump(self, obj):
		obj["s"] = self.s
	def draw(self):
		alpha = 2 * self.flife * (1 - self.flife)
		image.worlddraw("tremor-white", self.X, self.y, self.s, rotate = False, alpha = alpha)

class DrawFirstConvergence(Component):
	def __init__(self):
		self.nspoke = 32
	def init(self, ds = None, **kwargs):
		self.ds = ds or [random.uniform(40, 80) for _ in range(self.nspoke)]
	def dump(self, obj):
		obj["ds"] = self.ds
	def think(self, dt):
		targett = self.lifetime - self.t
		targetX = state.you.X + state.you.vx * targett / state.you.y
		targety = state.you.y + state.you.vy * targett
		for jspoke, d in enumerate(self.ds):
			if random.random() * 0.5 < dt:
				a = jspoke * math.tau / self.nspoke
				dX = d * (1 - self.flife) * math.sin(a) / state.you.y
				dy = d * (1 - self.flife) * math.cos(a)
				state.effects.append(Blob(X = targetX + dX, y = targety + dy))
	def draw(self):
		pass
	def die(self):
		from src.scenes import act2cutscene
		act2cutscene.playing = True
		background.wash()
	

class DrawBubble(Component):
	def init(self, color = None, **kwargs):
		self.color = color or (0, random.uniform(40, 100), random.uniform(20, 70))
	def dump(self, obj):
		obj["color"] = self.color
	def draw(self):
		p = window.screenpos(self.X, self.y)
		r = F(max(10 * self.flife, 1))
		pygame.draw.circle(window.screen, self.color, p, r, F(1))

class DrawWarpEffect(Component):
	def draw(self):
		p = window.screenpos(self.X, self.y)
		for d in (10, 20, 30):
			r = F(max(1, abs(40 * self.flife - d)))
			pygame.draw.circle(window.screen, (255, 255, 127), p, r, F(1))

class DrawBubbleChain(Component):
	def think(self, dt):
		if random.random() * 0.15 < dt:
			X = random.gauss(self.X, 0.3 / self.y)
			y = random.gauss(self.y, 0.3)
			state.effects.append(Bubble(X = X, y = y))
	def draw(self):
		pass

class DrawTeleport(Component):
	def init(self, targetid, **kwargs):
		self.targetid = targetid
	def dump(self, obj):
		obj["targetid"] = self.targetid
	def draw(self):
		target = get(self.targetid)
		if not target:
			return
		for d, s in [(-0.1, 3), (-0.05, 6), (0, 8), (0.05, 6), (0.1, 3)]:
			f = math.clamp(self.flife + d, 0, 1)
			X = self.X + f * (target.X - self.X)
			y = self.y + f * (target.y - self.y)
			pygame.draw.circle(window.screen, (255, 128, 255), window.screenpos(X, y), F(s), 0)

class DrawSlowTeleport(Component):
	def init(self, X1, y1, **kwargs):
		self.X1 = X1
		self.y1 = y1
	def dump(self, obj):
		obj["targetid"] = self.targetid
	def draw(self):
		for d, s in [(-0.1, 3), (-0.05, 6), (0, 8), (0.05, 6), (0.1, 3)]:
			f = math.clamp(self.flife + d, 0, 1)
			X = self.X + f * (self.X1 - self.X)
			y = self.y + f * (self.y1 - self.y)
			pygame.draw.circle(window.screen, (255, 128, 255), window.screenpos(X, y), F(s), 0)

# Base class for things
@HasId()
@HasType()
@KeepsTime()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(**kwargs)
		add(self)

@Alive()
@WorldBound()
@HasVelocity()
class WorldThing(Thing):
	pass

@HorizontalOscillation(2, 1)
@Hidden(settings.beacondetect)
@DrawHiddenRotatingImage("payload", 2.5)
class Payload(WorldThing):
	pass

@HorizontalOscillation(2, 1)
@Hidden(settings.beacondetect)
@DrawHiddenImage("batesship", 3)
class BatesShip(WorldThing):
	pass

@EmptyDrawHUD()
@HasSignificance()
@DiesAtCore()
@WinsAtCore()
@LeavesCorpse()
class Ship(WorldThing):
	pass

@HasHealth(5)
@HasMaximumHorizontalVelocity(6)
@HasMaximumVerticalVelocity(6)
@DrawImage("trainer")
@IgnoresNetwork()
class Trainer(Ship):
	pass

@HasHealth(3)
@Drifts()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(20)
@VerticalWeight()
@HasMaximumVerticalVelocity(10)
@DrawImageFlash("skiff")
@IgnoresNetwork()
@CantDeploy()
class Skiff(Ship):
	pass

@HasHealth(3)
@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight()
@HasMaximumVerticalVelocity(3)
@DrawImageFlash("mapper")
@IgnoresNetwork()
@CanDeploy()
@DeployFreeze()
@MapperDeploy()
class Mapper(Ship):
	pass

@HasHealth(3)
@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight()
@HasMaximumVerticalVelocity(3)
@DrawImageFlash("beacon")
@IgnoresNetwork()
@CanDeployOnce()
@DeployFreeze()
@BeaconDeploy()
class Beacon(Ship):
	pass

@HasHealth(3)
@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight()
@HasMaximumVerticalVelocity(3)
@DrawImageFlash("warp")
@IgnoresNetwork()
@WarpDeploy()
class Warp(Ship):
	pass

@HasHealth(11)
@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight()
@HasMaximumVerticalVelocity(3)
@DrawImageFlash("heavy")
@IgnoresNetwork()
@CantDeploy()
class Heavy(Ship):
	pass

@HasHealth(3)
@Drifts()
@HasMaximumHorizontalVelocity(20)
@VerticalWeight()
@HasMaximumVerticalVelocity(10)
@DrawImageFlash("beaconskiff")
@IgnoresNetwork()
@CanDeployOnce()
@DeployFreeze()
@BeaconDeploy()
class BeaconSkiff(Ship):
	pass

@HasHealth(11)
@Drifts()
@HasMaximumHorizontalVelocity(20)
@VerticalWeight()
@HasMaximumVerticalVelocity(10)
@DrawImageFlash("heavyskiff")
@IgnoresNetwork()
@CantDeploy()
class HeavySkiff(Ship):
	pass

@HasHealth(11)
@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight()
@HasMaximumVerticalVelocity(3)
@DrawImageFlash("heavymapper")
@IgnoresNetwork()
@CanDeploy()
@DeployFreeze()
@MapperDeploy()
class HeavyMapper(Ship):
	pass

@HasHealth(3)
@Drifts()
@HasMaximumHorizontalVelocity(20)
@VerticalWeight()
@HasMaximumVerticalVelocity(10)
@DrawImageFlash("warpskiff")
@IgnoresNetwork()
@WarpDeploy()
class WarpSkiff(Ship):
	pass

@HasHealth(11)
@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight()
@HasMaximumVerticalVelocity(3)
@DrawImageFlash("heavybeacon")
@IgnoresNetwork()
@CanDeployOnce()
@DeployFreeze()
@BeaconDeploy()
class HeavyBeacon(Ship):
	pass

@HasHealth(11)
@Drifts()
@HasMaximumHorizontalVelocity(20)
@VerticalWeight()
@HasMaximumVerticalVelocity(10)
@DrawImageFlash("heavywarpskiff")
@IgnoresNetwork()
@WarpDeploy()
class HeavyWarpSkiff(Ship):
	pass

@HasHealth(11)
@Drifts()
@HasMaximumHorizontalVelocity(20)
@VerticalWeight()
@HasMaximumVerticalVelocity(10)
@DrawImageFlash("heavybeaconskiff")
@IgnoresNetwork()
@CanDeployOnce()
@DeployFreeze()
@BeaconDeploy()
class HeavyBeaconSkiff(Ship):
	pass

@HasHealth(11)
@Drifts()
@HasMaximumHorizontalVelocity(20)
@VerticalWeight()
@HasMaximumVerticalVelocity(10)
@DrawImageFlash("heavymapperskiff")
@IgnoresNetwork()
@CanDeploy()
@DeployFreeze()
@MapperDeploy()
class HeavyMapperSkiff(Ship):
	pass

@MovesCircularWithConstantSpeed(8, 0.2)
@DrawTremor()
class Tremor(WorldThing):
	hazardsize = 4

@MovesCircularWithConstantSpeed(8, 0.2)
@DrawSlash()
class Slash(WorldThing):
	hazardsize = 4
	dhp = 1

@DrawRung()
class Rung(WorldThing):
	hazardsize = 7
	dhp = 2

@DrawImage("mother", 6)
@IgnoresNetwork()
class Mother(WorldThing):
	pass


@Laddered()
@DrawFilament()
class Filament(Thing):
	pass

@Lifetime(1)
@DropsDown(10)
@DrawCorpse()
class Corpse(WorldThing):
	pass

@DrawTarget()
class Target(WorldThing):
	pass

@Alive()
@DrawTargetOverParent()
class ShipTarget(Thing):
	pass

@DrawBubbles()
class Bubbler(WorldThing):
	pass

@Hidden(20)
@DrawConvergence()
class Convergence(WorldThing):
	pass

@Lifetime(5)
@DrawFirstConvergence()
class FirstConvergence(WorldThing):
	pass

@Lifetime(1)
@DiesAtCore()
@DrawBubble()
class Bubble(WorldThing):
	pass

@Lifetime(2)
@DrawBlob()
class Blob(WorldThing):
	pass

@Lifetime(1)
@DrawWarpEffect()
class WarpEffect(WorldThing):
	pass

@Lifetime(5)
@Converges()
@DrawBubbleChain()
class BubbleChain(WorldThing):
	pass

@Lifetime(0.25)
@DrawTeleport()
class Teleport(WorldThing):
	pass

@Lifetime(5)
@DrawSlowTeleport()
class SlowTeleport(WorldThing):
	pass


def dump():
	obj = {}
	obj["nextthingid"] = nextthingid
	obj["things"] = {}
	for thingid, thing in things.items():
		data = {}
		thing.dump(data)
		obj["things"][thingid] = data
	return obj

def load(obj):
	global nextthingid
	things.clear()
	nextthingid = obj["nextthingid"]
	for thingid, data in obj["things"].items():
		things[thingid] = globals()[data["type"]](**data)


