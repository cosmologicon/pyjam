import os, pygame, random, json, math
from . import settings, pview, ptext, flake, background, view, frostscene, hud, scene
from .pview import T

class self:
	pass

def init():
	self.specs = None
	self.buttons = [
		hud.Button(((pview.w0 - 80, pview.h0 - 80), 50), "Back"),
	]
	self.designs = None
	self.Fspots = None
	self.jload = None
	self.a = 0


def rFspot(r, x0, y0, t0):
	dt = 0.001 * pygame.time.get_ticks() - t0
	y = y0 + 100 * dt + 25 * math.sin(1.234 * dt)
	x = x0 - 20 * dt + 50 * math.sin(0.987 * dt + 3.456)
	x *= r / 50
	y *= r / 50
	x %= 1.5 * pview.w0
	y %= 2 * pview.h0
	return (x - pview.w0 / 4, y - pview.h0 / 2), r

def load():
	if os.path.exists(settings.gallerydir):
		filenames = list(os.listdir(settings.gallerydir))
		random.shuffle(filenames)
		filenames = filenames[:100]
	else:
		filenames = []

	self.specs = []
	for filename in filenames:
		spec = json.load(open(os.path.join(settings.gallerydir, filename), "r"))
		self.specs.append(spec)
	assert self.specs
	while len(self.specs) < 100:
		self.specs += [json.loads(json.dumps(spec)) for spec in self.specs]
	self.designs = [flake.Design(spec["design"]) for spec in self.specs]
#	self.designs = []
#	for jspec in range(100):
#		spec = json.loads(json.dumps(self.specs[jspec % len(self.specs)]))
#		spec = self.specs[jspec % len(self.specs)]
#		print(jspec, spec)
#		self.designs.append(flake.Design(spec["design"]))
	for design in self.designs:
		design.s = T(80)
	self.rFspotspecs = [
		(random.uniform(35, 65), random.uniform(0, 10000), random.uniform(0, 10000), random.uniform(0, 2))
		for _ in range(100)
	]
	self.rFspotspecs.sort()


def think(dt, controls):
	if self.specs is None:
		load()
	background.update(dt, (20, 20, 60))

	self.jbutton = None
	if self.jload is None:
		for jbutton, button in enumerate(self.buttons):
			if button.contains(controls.mpos):
				self.jbutton = jbutton
		if controls.mdown:
			if self.jbutton is not None:
				onclick(self.buttons[self.jbutton])
			else:
				for jspot, rFspotspec in reversed(list(enumerate(self.rFspotspecs))):
					pos, r = rFspot(*rFspotspec)
					if math.distance(pos, controls.mpos) < r:
						loaddesign(jspot)
						break
	if self.jload is not None and self.up:
		self.a = math.approach(self.a, 1, 3 * dt)
		self.Fload = view.Fspotapproach(self.Fload, ((360, 360), 320), 10 * dt)
		if self.a == 1 and controls.mdown:
			self.up = False
	if self.jload is not None and not self.up:
		self.a = math.approach(self.a, 0, 3 * dt)
		Fspot0 = rFspot(*self.rFspotspecs[self.jload])
		self.Fload = view.Fspotapproach(self.Fload, Fspot0, 20 * dt)
		if self.a == 0:
			design = self.designs[self.jload % len(self.designs)]
			design.s = T(80)
			design.undraw()
			self.jload = None

def onclick(button):
	if button.text == "Back":
		scene.push(frostscene, depth1 = 3)

def loaddesign(jspot):
	self.jload = jspot
	self.Fload = rFspot(*self.rFspotspecs[jspot])
	design = self.designs[self.jload % len(self.designs)]
	design.s = T(320)
	design.undraw()
	self.up = True
	self.a = 0

def draw():
	background.draw()
	for jspot, rFspotspec in enumerate(self.rFspotspecs):
		if jspot == self.jload:
			continue
		Fspot = rFspot(*rFspotspec)
		omega = 100 * (math.phi * jspot % 1 - 0.5)
		theta = omega * pygame.time.get_ticks() * 0.001
		self.designs[jspot % len(self.designs)].draw(Fspot, theta)
	if self.jload is None:
		for jbutton, button in enumerate(self.buttons):
			button.draw(lit = (jbutton == self.jbutton))
	if self.jload is not None:
		alpha = math.clamp(200 * self.a, 0, 200)
		pview.fill((0, 0, 60, alpha))
		self.designs[self.jload % len(self.designs)].draw(self.Fload)
		spec = self.specs[self.jload % len(self.designs)]
		if spec["designname"]:
			ptext.draw(spec["designname"], midbottom = T(940, 300), width = T(380),
				color = "#aabbff", shade = 1,
				fontsize = T(80), fontname = "ChelaOne", shadow = (1, 1), alpha = self.a
			)
		if spec["makername"]:
			ptext.draw("by", center = T(940, 360), color = "#ffffaa", shade = 1,
				fontsize = T(54), fontname = "ChelaOne", shadow = (1, 1), alpha = self.a
			)
			ptext.draw(spec["makername"], midtop = T(940, 420), width = T(380),
				color = "#aabbff", shade = 1,
				fontsize = T(80), fontname = "ChelaOne", shadow = (1, 1), alpha = self.a
			)
		


