from __future__ import division
import pygame, math, random
from . import view, control, state, blob, img, settings, bounce, mechanics, util, sound
from .util import F
from .enco import Component

class Lives(Component):
	def addtostate(self):
		state.thinkers.append(self)
	def setstate(self, alive = True, t = 0, **kw):
		self.alive = alive
		self.t = t
	def think(self, dt):
		self.t += dt
	def die(self):
		self.alive = False

class LivesToHatch(Lives):
	def think(self, dt):
		for _ in range(state.cell.countflavors(1)):
			dt *= 2.0
		self.t += dt

class Lifetime(Component):
	def setstate(self, lifetime = 1, preserved = False, **kw):
		self.lifetime = lifetime
		self.flife = math.clamp(self.t / self.lifetime, 0, 1)
		self.preserved = preserved
	def think(self, dt):
		if not self.alive:
			return
		self.flife = math.clamp(self.t / self.lifetime, 0, 1)
		if self.t > self.lifetime and not self.preserved:
			self.die()

class WorldBound(Component):
	def setstate(self, x = 0, y = 0, **kw):
		self.x = x
		self.y = y
	def scootch(self, dx, dy):
		self.x += dx
		self.y += dy
	def distanceto(self, pos):
		x, y = pos
		return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

class Drawable(Component):
	def addtostate(self):
		state.drawables.append(self)

class Collidable(Component):
	def setstate(self, rcollide = 10, mass = 10, **kw):
		self.rcollide = rcollide
		self.mass = mass
	def getcollidespec(self):
		return self.x, self.y, self.rcollide, self.mass
	def constraintoworld(self):
		d = math.sqrt(self.x ** 2 + self.y ** 2)
		r = state.Rlevel - self.rcollide
		if d > r:
			f = r / d - 1
			self.scootch(self.x * f, self.y * f)
	def draw(self):
		if settings.showbox:
			pygame.draw.circle(view.screen, (255, 255, 255),
				view.screenpos((self.x, self.y)), view.screenlength(self.rcollide), 1)

class WorldCollidable(Collidable):
	def addtostate(self):
		state.colliders.append(self)

class Kickable(Component):
	def setstate(self, ix = 0, iy = 0, **kw):
		self.ix = ix
		self.iy = iy
	def kick(self, ix, iy):
		self.ix += ix
		self.iy += iy
	def think(self, dt):
		if self.ix or self.iy:
			self.scootch(self.ix * dt, self.iy * dt)
			f = math.exp(-2 * dt)
			self.ix *= f
			self.iy *= f

class Unkickable(Component):
	def kick(self, ix, iy):
		pass

class CarriesViruses(Component):
	def setstate(self, carrytype, ncarried = 3, **kw):
		self.ncarried = ncarried
		self.carrytype = carrytype
	def die(self):
		theta = random.angle()
		for j in range(self.ncarried):
			dx = math.sin(theta + j * math.tau / self.ncarried)
			dy = math.cos(theta + j * math.tau / self.ncarried)
			ant = self.carrytype(x = self.x + 2 * dx, y = self.y + 2 * dy)
			ant.target = self.target
			ant.kick(50 * dx, 50 * dy)
			ant.addtostate()

class Mouseable(Component):
	def addtostate(self):
		state.mouseables.append(self)
	def setstate(self, rmouse = 5, **kw):
		self.rmouse = rmouse
	def within(self, pos):
		x, y = pos
		return (x - self.x) ** 2 + (y - self.y) ** 2 < self.rmouse ** 2
	def onhover(self):
		pass
	def ondrag(self, pos):
		pass
	def onmousedown(self):
		pass
	def onclick(self):
		pass
	def onrdown(self):
		pass
	def flavors(self):
		return None

class Shootable(Component):
	def addtostate(self):
		state.shootables.append(self)
	def setstate(self, hp = 1, **kw):
		self.hp = hp
	def shoot(self, dhp, rewardprob = (0, 0)):
		if self.hp <= 0:
			return
		self.hp -= dhp
		if self.hp <= 0:
			self.die()
			p1, p2 = rewardprob
			if random.random() < p2:
				ATP2(x = self.x, y = self.y).addtostate()
			elif random.random() < p1:
				ATP1(x = self.x, y = self.y).addtostate()

class Draggable(Component):
	def onmousedown(self):
		if control.cursor is None and not self.disabled:
			control.cursor = self
			sound.playsfx("blobup")
			state.removeobj(control.cursor)
			control.done.add("adrag")

class RightClickToSplit(Component):
	def onrdown(self):
		if len(self.slots) < 2:
			return
		state.removeobj(self)
		for obj in self.slots:
			t = obj.totower()
			t.kick(*util.norm(obj.x - self.x, obj.y - self.y, 20))
			t.addtostate()

class ContainedDraggable(Component):
	def onmousedown(self):
		if self.container.disabled:
			return
		if control.cursor is None:
			if (len(self.container.slots) == 1 or settings.pulltower) and self.container.mass < 9999:
				control.cursor = self.container
				if self.container is state.cell:
					control.done.add("cdrag")
				else:
					control.done.add("adrag")
			else:
				self.container.remove(self)
				control.cursor = self.totower()
			state.removeobj(control.cursor)
			sound.playsfx("blobup")
	def onclick(self):
		self.container.onclick()

class DrawCircle(Component):
	def setstate(self, r = 10, color = (100, 0, 0), **kw):
		self.r = r
		self.color = color
	def draw(self):
		pygame.draw.circle(view.screen, self.color, view.screenpos((self.x, self.y)), view.screenlength(self.r))

class DrawOrganelle(Component):
	def setstate(self, r = 10, **kw):
		self.r = r
		self.xjitter, self.yjitter = 0, 0
	def think(self, dt):
		self.xjitter += 10 * dt * random.uniform(-1, 1)
		self.yjitter += 10 * dt * random.uniform(-1, 1)
		f = math.exp(-1 * dt)
		self.xjitter *= f
		self.yjitter *= f
	def draw(self):
		imgname = "organelle-" + "XYZ"[self.flavor]
		img.drawworld(imgname, (self.x + self.xjitter, self.y + self.yjitter), self.r)

class DrawEgg(Component):
	def setstate(self, r = 10, **kw):
		self.r = r
		self.xjitter, self.yjitter = 0, 0
		self.imgname = "egg"
	def think(self, dt):
		self.xjitter += 10 * dt * random.uniform(-1, 1)
		self.yjitter += 10 * dt * random.uniform(-1, 1)
		f = math.exp(-1 * dt)
		self.xjitter *= f
		self.yjitter *= f
	def draw(self):
		r = (0.8 + 0.4 * math.sin(2.5 * self.t)) * self.r
		fstretch = math.exp(0.2 * math.sin(3.5 * self.t))
		img.drawworld(self.imgname, (self.x + self.xjitter, self.y + self.yjitter), r, fstretch = fstretch)

class DrawVirus(Component):
	def setstate(self, r = 10, imgname = "virus", **kw):
		self.r = r
		self.tdraw0 = random.uniform(0, 1000)
		self.imgname = imgname
		self.fstretch = 1
		self.angle = 0
		self.imgdy = 0
	def think(self, dt):
		tdraw = self.tdraw0 + self.t
		self.fstretch = math.exp(0.3 * math.sin(10 * tdraw))
		self.angle = 15 * math.sin(2 * tdraw)
		self.imgdy = 0.3 * self.r * math.sin(10 * tdraw)
	def draw(self):
		if settings.virusbounce:
			img.drawworld(self.imgname, (self.x, self.y + self.imgdy), self.r, fstretch = self.fstretch, angle = self.angle)
		else:
			img.drawworld(self.imgname, (self.x, self.y), self.r)


class DrawCorpse(Component):
	def setstate(self, x, y, imgname, r, fstretch = 1, angle = 0, **kw):
		self.x = x
		self.y = y
		self.imgname = imgname
		self.fstretch = fstretch
		self.angle = angle
		self.r = r
	def draw(self):
		r = self.r * (1 + self.flife)
		alpha = 1 - self.flife
		img.drawworld(self.imgname, (self.x, self.y), r, fstretch = self.fstretch, angle = self.angle, alpha = alpha)

class DrawInjection(Component):
	def setstate(self, x0, y0, x1, y1, imgname, r, fstretch = 1, angle = 0, **kw):
		self.x0, self.y0 = x0, y0
		self.x1, self.y1 = x1, y1
		self.imgname = imgname
		self.fstretch = fstretch
		self.angle = angle
		self.r = r
	def draw(self):
		f, df = self.flife, 1 - self.flife
		x = self.x0 * df + self.x1 * f
		y = self.y0 * df + self.y1 * f
		r = self.r * df
		img.drawworld(self.imgname, (x, y), r, fstretch = self.fstretch, angle = self.angle)

class LeavesCorpse(Component):
	def die(self):
		if self.hp <= 0:
			Corpse(self).addtostate()

class InfiltratesOnArrival(Component):
	def arrive(self):
		if self.target:
			Injection(self, self.target).addtostate()

class DrawBlob(Component):
	def setstate(self, rblob = 10, nblob = 3, color = (0, 120, 120), **kw):
		self.rblob = rblob
		self.nblob = nblob
		self.color = color
		self.blobspecs = [(
			random.uniform(0, math.tau),
			random.uniform(0.6, 1) * (-1 if j % 2 else 1),
			random.uniform(0.6, 0.8),
		) for j in range(self.nblob)]
	def draw(self):
		blobspec = [(self.x, self.y, 2 * self.rblob, 1)]
		for theta0, dtheta, fr in self.blobspecs:
			theta = theta0 + self.t * dtheta
			x = self.x + fr * self.rblob * math.sin(theta)
			y = self.y + fr * self.rblob * math.cos(theta)
			blobspec.append((x, y, 0.8 * self.rblob, 0.5))
		view.drawblob(blobspec, color = self.color)

class Hatches(Component):
	def die(self):
		if self not in self.container.slots:
			return
		organelle = Organelle(flavor = self.flavor, container = self.container, x = self.x, y = self.y)
		self.container.remove(self)
		self.container.add(organelle)
		organelle.addtostate()

class HasSlots(Component):
	def setstate(self, slots = None, nslot = 3, **kw):
		self.slots = slots or []
		self.nslot = nslot
	def isfull(self):
		return len(self.slots) >= self.nslot
	def add(self, obj):
		self.slots.append(obj)
	def remove(self, obj):
		self.slots.remove(obj)
	def think(self, dt):
		f = 1 - math.exp(-dt)
		for obj in self.slots:
			obj.x += (self.x - obj.x) * f
			obj.y += (self.y - obj.y) * f
		if len(self.slots) > 1:
			bounce.adjust(self.slots, dt)
	def draw(self):
		for obj in self.slots:
			obj.draw()
	def scootch(self, dx, dy):
		for obj in self.slots:
			obj.scootch(dx, dy)
	def flavors(self):
		return "".join(sorted("XYZ"[obj.flavor] for obj in self.slots))

class Buildable(Component):
	def addtostate(self):
		state.buildables.append(self)
	def cantake(self, obj):
		from . import progress
		maxslots = max(len(formula) for formula in progress.learned)
		if len(obj.slots) + len(self.slots) > maxslots or self.disabled:
			return False
		dx, dy = obj.x - self.x, obj.y - self.y
		r = self.rcollide + obj.rcollide
		return dx ** 2 + dy ** 2 < r ** 2

class ResizesWithSlots(Component):
	def add(self, obj):
		self.resize()
	def remove(self, obj):
		self.resize()
	def resize(self):
		self.mass = 4
		# TODO: better resizing algorithm
		if self.slots:
			r = 2 + sum(obj.rcollide ** 1.8 for obj in self.slots) ** (1/1.8)
			self.mass += sum(obj.mass for obj in self.slots)
		else:
			r = 4
		self.rcollide = 1.2 * r
		self.rmouse = 1.2 * r
		self.rblob = r

# Move from p0 to p1 by an amount d, and return if you're now closer than dr
def approachpos(p0, p1, d, dr):
	x0, y0 = p0
	x1, y1 = p1
	dx, dy = x1 - x0, y1 - y0
	dp = math.sqrt(dx ** 2 + dy ** 2)
	if dp == 0:
		return x0, y0, True
	return x0 + dx * d / dp, y0 + dy * d / dp, (dp - dr < d)

class DisappearsToCell(Component):
	def setstate(self, approaching = False, **kw):
		self.approaching = approaching
#		self.preserved = True
#		self.approaching = True
		self.target = None
	def onhover(self):
		if self.target:
			return
		self.preserved = True
		self.approaching = True
		self.target = state.cell
	def think(self, dt):
		if not self.approaching or not self.alive or not self.target:
			return
		self.x, self.y, arrived = approachpos((self.x, self.y), (self.target.x, self.target.y), dt * 300, self.target.rcollide)
		if arrived:
			self.arrive()

class TargetsThing(Component):
	def setstate(self, target = None, speed = 10, **kw):
		self.target = target
		self.speed = speed
	def think(self, dt):
		if self.alive and self.target is not None:
			dr = self.rcollide + self.target.rcollide
			self.x, self.y, arrived = approachpos((self.x, self.y), (self.target.x, self.target.y), self.speed * dt, dr)
			if arrived:
				self.arrive()

class KicksToTarget(Component):
	def setstate(self, tkick, **kw):
		self.tkick = tkick
		self.kicktimer = random.uniform(0.8, 1.2) * self.tkick
	def think(self, dt):
		self.kicktimer -= dt
		if self.kicktimer <= 0:
			dx = self.target.x - self.x + random.uniform(-30, 30)
			dy = self.target.y - self.y + random.uniform(-30, 30)
			self.kick(*util.norm(dx, dy, 100))
			self.kicktimer = random.uniform(0.8, 1.2) * self.tkick

class HurtsTarget(Component):
	def setstate(self, dhp, rewardprob = (0, 0), **kw):
		self.dhp = dhp
		self.rewardprob = rewardprob
	def arrive(self):
		self.target.shoot(self.dhp, self.rewardprob)

class ExplodesOnArrival(Component):
	def setstate(self, shockdhp, wavesize, shockkick = 0, **kw):
		self.shockdhp = shockdhp
		self.wavesize = wavesize
		self.shockkick = shockkick
	def arrive(self):
		Shockwave(x = self.target.x, y = self.target.y,
			dhp = self.shockdhp, kick = self.shockkick, wavesize = self.wavesize).addtostate()

class TargetsTower(Component):
	def think(self, dt):
		if random.random() < dt:
			self.target = None
			r2 = 50 ** 2
			for obj in state.buildables:
				if obj.disabled:
					continue
				dx, dy = obj.x - self.x, obj.y - self.y
				d2 = dx ** 2 + dy ** 2
				if d2 < r2:
					self.target, r2 = obj, d2
			if self.target is None:
				self.target = state.cell

class DiesOnArrival(Component):
	def arrive(self):
		self.die()

class HarmsOnArrival(Component):
	def setstate(self, damage = 1, **kw):
		self.damage = damage
	def arrive(self):
		if self.target is state.cell:
			state.takedamage(self.damage)

class DisablesOnArrival(Component):
	def setstate(self, tdisable, **kw):
		self.tdisable = tdisable
	def arrive(self):
		if self.target and self.target is not state.cell:
			self.target.disabled = self.tdisable

class HealsOnArrival(Component):
	def setstate(self, dheal, **kw):
		self.dheal = dheal
	def arrive(self):
		self.target.disabled = max(0, self.target.disabled - self.dheal)

class KicksOnArrival(Component):
	def setstate(self, kick = 0, **kw):
		self.kick = kick
	def arrive(self):
		if not self.kick or not self.target or not self.target.alive:
			return
		self.target.kick(*util.norm(self.target.x - self.x, self.target.y - self.y, self.kick))

class CleansOnDeath(Component):
	def addtostate(self):
		state.bosses.append(self)
	def die(self):
		if all(boss is self or boss.alive == False for boss in state.bosses):
			for obj in state.shootables:
				if obj.alive:
					obj.die()

class BossStages(Component):
	def setstate(self, stages, rstages, **kw):
		self.stages = stages
		self.rstages = rstages
		self.stage = 0
	def think(self, dt):
		if self.stage >= len(self.stages):
			return
	def shoot(self, *args):
		if self.stage < len(self.stages) and self.hp <= self.stages[self.stage]:
			self.advance()
			self.stage += 1
		if self.stage < len(self.stages):
			self.r = self.rcollide = 2.5 * self.rstages[self.stage]
	def advance(self):
		self.shedcorpse(self.rstages[self.stage])
		sound.playsfx("bigdie")
	def shedcorpse(self, rstage):
		BossCorpse(self, rstage).addtostate()
	def draw(self):
		for j, rstage in enumerate(self.rstages[self.stage:]):
			r = 2.5 * rstage
			angle = self.t * 200 / math.sqrt(rstage) * [-1, 1][j % 2]
			imgname = "saw%d" % rstage
			img.drawworld(imgname, (self.x, self.y), r, angle = angle)


class SpawnsAnts(Component):
	def setstate(self, spawntime = 1, spawnstart = 20, **kw):
		self.lastspawn = spawnstart
		self.spawntime = spawntime
	def think(self, dt):
		while self.lastspawn < self.t:
			self.spawn()
			self.lastspawn += self.spawntime
	def spawn(self):
		ant = Ant(x = self.x + random.uniform(-10, 10), y = self.y + random.uniform(-10, 10))
		ant.target = state.cell
		ant.addtostate()

class CirclesArena(Component):
	def setstate(self, rpath, drpath, vpath, **kw):
		self.rpath = rpath
		self.drpath = drpath
		self.vpath = vpath
		self.theta = 0
	def think(self, dt):
		phi = self.theta / ((1 + math.sqrt(5)) / 2)
		R = self.rpath + self.drpath * math.sin(phi) + max(0, 20 - self.t) * 10
		self.theta += self.vpath * dt / R
		self.x = R * math.sin(self.theta)
		self.y = R * math.cos(self.theta)


class GetsATP1(Component):
	def arrive(self):
		state.atp[0] += 1

class GetsATP2(Component):
	def arrive(self):
		state.atp[1] += 1

class FollowsRecipe(Component):
	def add(self, obj):
		self.fullreset()
	def reset(self):
		from . import recipe
		recipe.reset(self)
	def fullreset(self):
		from . import recipe
		recipe.fullreset(self)
	def think(self, dt):
		from . import recipe
		recipe.think(self, dt)
	def onclick(self):
		from . import recipe
		recipe.onclick(self)

class DrawLaser(Component):
	def setstate(self, x0, x1, y0, y1, color = (255, 255, 255), **kw):
		self.x0 = x0
		self.y0 = y0
		self.x1 = x1
		self.y1 = y1
		self.color = color
	def draw(self):
		pygame.draw.aaline(view.screen, self.color,
			view.screenpos((self.x0, self.y0)),
			view.screenpos((self.x1, self.y1)),
			view.screenlength(1))

class DrawShockwave(Component):
	def setstate(self, wavesize, color = (255, 255, 255), **kw):
		self.wavesize = wavesize
		self.color = color
	def draw(self):
		r = max(F(2), F(self.wavesize * self.flife))
		pygame.draw.circle(view.screen, self.color, view.screenpos((self.x, self.y)), r, F(2))

class ShocksEnemies(Component):
	def setstate(self, dhp, kick = 0, rewardprob = (0, 0), **kw):
		self.dhp = dhp
		self.kick = kick
		self.rewardprob = rewardprob
		self.hits = []
	def think(self, dt):
		r = self.wavesize * self.flife
		for enemy in state.shootables:
			if enemy in self.hits or not enemy.alive:
				continue
			dx, dy = enemy.x - self.x, enemy.y - self.y
			if dx ** 2 + dy ** 2 < r ** 2:
				enemy.shoot(self.dhp, self.rewardprob)
				enemy.kick(*util.norm(dx, dy, self.kick))

@Lives()
@WorldBound()
@Drawable()
@DrawBlob()
@HasSlots()
@Buildable()
@WorldCollidable()
class Amoeba(object):
	def __init__(self, **kw):
		self.setstate(
			rcollide = 20, mass = 10000000,
			rblob = 20,
			nblob = 18,
			color = (0, 100, 100),
		**kw)
		self.disabled = False
	def flavors(self):
		return None
	def countflavors(self, n):
		return sum(isinstance(obj, Organelle) and obj.flavor == n for obj in self.slots)

@Lives()
@WorldBound()
@Mouseable()
@Draggable()
@RightClickToSplit()
@Kickable()
@Drawable()
@DrawBlob()
@HasSlots()
@Buildable()
@ResizesWithSlots()
@WorldCollidable()
@FollowsRecipe()
class Tower(object):
	def __init__(self, color = None, **kw):
		color = color or (0, 100, 100)
		self.setstate(
			rcollide = 20, mass = 10,
			rblob = 20,
			nblob = 18,
			color = color,
		**kw)
		self.targetcolor = None
		self.disabled = False
	def think(self, dt):
		from . import recipe
		self.targetcolor = recipe.getcolor(self)
		if self.disabled:
			tr, tg, tb = self.targetcolor
			self.targetcolor = tr // 3, tg // 3, tb // 3
		if self.targetcolor is not None and self.color != self.targetcolor:
			d = int(max(100 * dt, 1))
			self.color = tuple(math.clamp(y, x - d, x + d) for x, y in zip(self.color, self.targetcolor))

@Lives()
@Lifetime()
@WorldBound()
@Drawable()
@Mouseable()
@Kickable()
@DisappearsToCell()
@DiesOnArrival()
@DrawCircle()
@GetsATP1()
class ATP1(object):
	def __init__(self, **kw):
		self.setstate(
			color = (200, 200, 0),
			r = 4, rmouse = 24,
			lifetime = 100,
			**kw)

@Lives()
@Lifetime()
@WorldBound()
@Drawable()
@Mouseable()
@Kickable()
@DisappearsToCell()
@DiesOnArrival()
@DrawCircle()
@GetsATP2()
class ATP2(object):
	def __init__(self, **kw):
		self.setstate(
			color = (250, 150, 0),
			r = 4, rmouse = 24,
			lifetime = 100,
			**kw)

@Lives()
@WorldBound()
@Mouseable()
@ContainedDraggable()
@DrawOrganelle()
@Collidable()
class Organelle(object):
	def __init__(self, flavor, container, x = None, y = None, **kw):
		color = {
			0: (255, 0, 0),
			1: (0, 255, 0),
			2: (100, 100, 255),
		}[flavor]
		self.container = container
		if x is None:
			x = container.x + random.uniform(-1, 1)
		if y is None:
			y = container.y + random.uniform(-1, 1)
		self.setstate(
			rcollide = 6, mass = 10,
			rblob = 6, rmouse = 6,
			nblob = 0,
			r = 6, color = color,
			x = x, y = y,
			**kw)
		self.flavor = flavor
	def totower(self):
		tower = Tower(x = self.x, y = self.y, color = self.container.color)
		tower.add(self)
		self.container = tower
		return tower
	def flavors(self):
		return self.container.flavors()

@LivesToHatch()
@Lifetime()
@WorldBound()
@DrawEgg()
@Collidable()
@Hatches()
@LeavesCorpse()
class Egg(object):
	def __init__(self, flavor, container, **kw):
		self.container = container
		color = {
			0: (255, 0, 0, 120),
			1: (0, 255, 0, 120),
			2: (100, 100, 255, 120),
		}[flavor]
		thatch = [mechanics.Xthatch, mechanics.Ythatch, mechanics.Zthatch][flavor]
		self.setstate(
			rcollide = 8,
			r = 8, color = color,
			lifetime = thatch,
			x = container.x + random.uniform(-1, 1),
			y = container.y + random.uniform(-1, 1),
			**kw)
		self.flavor = flavor
		self.hp = 0
		self.imgdy = 0
		self.fstretch = 1
		self.angle = 0
	

@Lives()
@WorldBound()
@Drawable()
@Kickable()
@TargetsThing()
@DiesOnArrival()
@HarmsOnArrival()
@InfiltratesOnArrival()
@Shootable()
@DrawVirus()
@LeavesCorpse()
@WorldCollidable()
class Ant(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.anthp,
			speed = random.uniform(0.7, 1.3) * mechanics.antspeed,
			damage = mechanics.antdamage,
			rcollide = mechanics.antsize, mass = 10,
			r = mechanics.antsize, color = (255, 255, 255),
			imgname = "virusA",
			**kw)

@Lives()
@WorldBound()
@Drawable()
@Kickable()
@TargetsThing()
@TargetsTower()
@DiesOnArrival()
@HarmsOnArrival()
@DisablesOnArrival()
@InfiltratesOnArrival()
@Shootable()
@DrawVirus()
@LeavesCorpse()
@WorldCollidable()
class Bee(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.beehp,
			speed = random.uniform(4, 6),
			rcollide = 6, mass = 10,
			r = 6, color = (255, 255, 0),
			tdisable = mechanics.beetdisable,
			imgname = "virusB",
			**kw)

@Lives()
@WorldBound()
@Drawable()
@Kickable()
@TargetsThing()
@KicksToTarget()
@DiesOnArrival()
@HarmsOnArrival()
@InfiltratesOnArrival()
@Shootable()
@DrawVirus()
@LeavesCorpse()
@WorldCollidable()
class Flea(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.fleahp,
			damage = mechanics.fleadamage,
			speed = 0, tkick = mechanics.fleatkick,
			rcollide = 9, mass = 50,
			r = 9, color = (255, 255, 0),
			imgname = "virusC",
			**kw)

@Lives()
@WorldBound()
@Drawable()
@Kickable()
@TargetsThing()
@DiesOnArrival()
@HarmsOnArrival()
@InfiltratesOnArrival()
@Shootable()
@DrawVirus()
@LeavesCorpse()
@WorldCollidable()
class Weevil(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.weevilhp,
			damage = mechanics.weevildamage,
			speed = mechanics.weevilspeed,
			rcollide = mechanics.weevilsize, mass = 60,
			r = mechanics.weevilsize, color = (255, 255, 0),
			imgname = "virusD",
			**kw)


@Lives()
@WorldBound()
@Drawable()
@Kickable()
@TargetsThing()
@DiesOnArrival()
@HarmsOnArrival()
@Shootable()
@DrawVirus()
@CarriesViruses()
@LeavesCorpse()
@WorldCollidable()
class LargeAnt(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.Lanthp,
			speed = random.uniform(0.8, 1.2) * mechanics.Lantspeed,
			damage = mechanics.Lantdamage,
			rcollide = mechanics.Lantsize, mass = 100,
			r = mechanics.Lantsize,
			ncarried = mechanics.Lantcarried, carrytype = Ant,
			imgname = "virusA",
			**kw)

@Lives()
@WorldBound()
@Drawable()
@Kickable()
@TargetsThing()
@DiesOnArrival()
@HarmsOnArrival()
@Shootable()
@DrawVirus()
@CarriesViruses()
@LeavesCorpse()
@WorldCollidable()
class LargeBee(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.Lbeehp,
			speed = random.uniform(0.8, 1.2) * mechanics.Lbeespeed,
			damage = mechanics.Lbeedamage,
			rcollide = mechanics.Lbeesize, mass = 100,
			r = mechanics.Lbeesize,
			ncarried = mechanics.Lbeecarried, carrytype = Bee,
			imgname = "virusB",
			**kw)

@Lives()
@WorldBound()
@Drawable()
@Kickable()
@TargetsThing()
@DiesOnArrival()
@HarmsOnArrival()
@Shootable()
@DrawVirus()
@CarriesViruses()
@LeavesCorpse()
@WorldCollidable()
class LargeWeevil(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.Lweevilhp,
			speed = random.uniform(0.8, 1.2) * mechanics.Lweevilspeed,
			damage = mechanics.Lweevildamage,
			rcollide = mechanics.Lweevilsize, mass = 200,
			r = mechanics.Lweevilsize,
			ncarried = mechanics.Lweevilcarried, carrytype = Weevil,
			imgname = "virusD",
			**kw)

@Lives()
@WorldBound()
@Drawable()
@Unkickable()
@Shootable()
@BossStages()
@SpawnsAnts()
@CleansOnDeath()
@WorldCollidable()
@CirclesArena()
class Wasp(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.wasphp,
			spawntime = mechanics.waspspawntime,
			rpath = 160, drpath = 80, vpath = mechanics.waspspeed,
			rcollide = 25, mass = 10000000,
			stages = mechanics.waspstages,
			rstages = mechanics.waspsizes,
			r = 25,
			**kw)
		self.think(0)
	def advance(self):
		self.vpath *= 2
		self.spawntime /= 2

@Lives()
@WorldBound()
@Drawable()
@Unkickable()
@Shootable()
@BossStages()
@SpawnsAnts()
@CleansOnDeath()
@WorldCollidable()
@CirclesArena()
class Hornet(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.hornethp,
			spawntime = mechanics.hornetspawntime,
			rpath = 160, drpath = 80, vpath = mechanics.hornetspeed,
			rcollide = 25, mass = 10000000,
			stages = mechanics.hornetstages,
			rstages = mechanics.hornetsizes,
			r = 25,
			**kw)
		self.think(0)
	def advance(self):
		self.vpath *= 2
		self.spawntime /= 2

@Lives()
@WorldBound()
@Drawable()
@Unkickable()
@Shootable()
@BossStages()
@SpawnsAnts()
@CleansOnDeath()
@WorldCollidable()
@CirclesArena()
class Cricket(object):
	def __init__(self, **kw):
		self.setstate(
			hp = mechanics.crickethp,
			spawntime = mechanics.cricketspawntime,
			rpath = 200, drpath = 100, vpath = mechanics.cricketspeed,
			rcollide = 25, mass = 10000000,
			stages = mechanics.cricketstages,
			rstages = mechanics.cricketsizes,
			r = 25,
			**kw)
		self.think(0)
	def advance(self):
		self.vpath *= 2
		self.spawntime /= 2


@Lives()
@WorldBound()
@Drawable()
@Unkickable()
@Shootable()
@BossStages()
@SpawnsAnts()
@CleansOnDeath()
@WorldCollidable()
@CirclesArena()
class Ladybug(object):
	def __init__(self, hp, spawntime, stages, sizes, speed, **kw):
		self.setstate(
			hp = hp,
			spawntime = spawntime,
			rpath = 160, drpath = 80, vpath = speed,
			rcollide = 25, mass = 10000000,
			stages = stages,
			rstages = sizes,
			r = 25,
			**kw)
		self.think(0)
	def advance(self):
		self.vpath *= 2
		self.spawntime /= 2

@Lives()
@Lifetime()
@Drawable()
@DrawLaser()
class Laser(object):
	def __init__(self, obj0, obj1, color = (255, 255, 255), **kw):
		self.setstate(
			lifetime = 0.2,
			x0 = obj0.x, y0 = obj0.y,
			x1 = obj1.x, y1 = obj1.y,
			color = color,
			**kw)

@Lives()
@Lifetime()
@WorldBound()
@Collidable()
@Drawable()
@DrawCircle()
@TargetsThing()
@HurtsTarget()
@KicksOnArrival()
@DiesOnArrival()
class Bullet(object):
	def __init__(self, obj, target, dhp, kick = 0, r = 3, color = (255, 100, 100), **kw):
		self.setstate(
			target = target, speed = mechanics.bulletspeed,
			lifetime = 5,
			dhp = dhp,
			kick = kick,
			r = r, rcollide = r,
			color = color,
			**kw)

@Lives()
@WorldBound()
@Collidable()
@Drawable()
@DrawCircle()
@TargetsThing()
@HurtsTarget()
@ExplodesOnArrival()
@DiesOnArrival()
class ExplodingBullet(object):
	def __init__(self, obj, target, dhp, shockdhp, wavesize, shockkick = 0, r = 3, color = (255, 100, 100), **kw):
		self.setstate(
			target = target, speed = mechanics.bulletspeed,
			dhp = dhp,
			shockdhp = shockdhp,
			wavesize = wavesize,
			shockkick = shockkick,
			r = r, rcollide = r,
			color = color,
			**kw)

@Lives()
@WorldBound()
@Collidable()
@Drawable()
@DrawCircle()
@TargetsThing()
@HealsOnArrival()
@DiesOnArrival()
class HealRay(object):
	def __init__(self, obj, target, dheal, **kw):
		self.setstate(
			target = target, speed = mechanics.healrayspeed,
			dheal = dheal,
			r = 3, rcollide = 3,
			color = (0, 100, 255),
			**kw)

@Lives()
@Lifetime()
@Drawable()
@DrawCorpse()
class Corpse(object):
	def __init__(self, obj, **kw):
		self.setstate(
			lifetime = 0.2,
			x = obj.x,
			y = obj.y + obj.imgdy,
			r = obj.r,
			imgname = obj.imgname,
			fstretch = obj.fstretch,
			angle = obj.angle,
			**kw)

@Lives()
@Lifetime()
@Drawable()
@DrawCorpse()
class BossCorpse(object):
	def __init__(self, obj, rstage, **kw):
		self.setstate(
			lifetime = 0.4,
			x = obj.x,
			y = obj.y,
			r = 2.5 * rstage,
			imgname = "saw%d" % rstage,
			**kw)

@Lives()
@Lifetime()
@Drawable()
@DrawInjection()
class Injection(object):
	def __init__(self, obj, target, **kw):
		self.setstate(
			lifetime = 0.3,
			x0 = obj.x, y0 = obj.y,
			x1 = target.x, y1 = target.y,
			r = obj.r,
			imgname = obj.imgname,
			fstretch = obj.fstretch,
			angle = obj.angle,
			**kw)

@Lives()
@WorldBound()
@Lifetime()
@Drawable()
@DrawShockwave()
@ShocksEnemies()
class Shockwave(object):
	def __init__(self, wavesize, **kw):
		self.setstate(
			wavesize = wavesize,
			lifetime = 0.5, color = (255, 255, 255),
			**kw)


