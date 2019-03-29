import pygame, math
from . import pview, ptext, background, settings, hud, scene, view, textscene, client
from .pview import T

class self:
	pass

Fspot1 = (640, 400), 200

def init(design, Fspot):
	self.design = design
	self.Fspot0 = Fspot
	self.Fspot = Fspot
	self.a = 0
	
	rect0 = pygame.Rect((0, 0, 320, 80))
	rect1 = pygame.Rect((0, 0, 320, 80))
	rect0.center = 240, 360
	rect1.center = pview.w0 - 240, 360
	self.boxes = [
		(rect0, "yourname"),
		(rect1, "designname"),
	]
	self.designname = ""
	self.jbox = None

	self.buttons = [
		hud.Button(((pview.w0 - 240 - 100, 620), 80), "YES\nUpload"),
		hud.Button(((pview.w0 - 240 + 100, 620), 80), "NO\nGo back"),
	]
	self.ending = False
	self.done = False


def think(dt, controls):
	background.update(dt)
	if self.ending:
		self.a = math.approach(self.a, 0, -4 * dt)
		self.Fspot = view.Fspotapproach(self.Fspot, self.Fspot0, 20 * dt)
		if not self.done and self.Fspot == self.Fspot0:
			self.done = True
			scene.pop()
	else:
		self.Fspot = view.Fspotapproach(self.Fspot, Fspot1, 10 * dt)
		if self.Fspot == Fspot1:
			self.a = math.approach(self.a, 1, 4 * dt)
	self.jbox = None
	self.jbutton = None

	if self.a == 1:
		for jbox, (box, name) in enumerate(self.boxes):
			if box.collidepoint(controls.mpos):
				self.jbox = jbox
		for jbutton, button in enumerate(self.buttons):
			if button.contains(controls.mpos):
				self.jbutton = jbutton

	if self.a == 1 and controls.mdown:
		if self.jbox == 0:
			scene.push(textscene, self.boxes[0][0], settings.yourname, updateyourname)
		if self.jbox == 1:
			scene.push(textscene, self.boxes[1][0], self.designname, updatedesignname)
		if self.jbutton is not None:
			onclick(self.buttons[self.jbutton])

def updateyourname(name):
	settings.yourname = name

def updatedesignname(name):
	self.designname = name

def onclick(button):
	if "YES" in button.text:
		client.upload(settings.yourname, self.designname, self.design)
		self.ending = True
	if "NO" in button.text:
		self.ending = True
	
def draw():
	background.draw()
	self.design.draw(self.Fspot)

	ptext.draw("Share this design to the public gallery", midtop = T(640, 20),
		color = "#ffffff", shade = 1,
		fontsize = T(80), fontname = "GermaniaOne", shadow = (1, 1), alpha = self.a
	)
	ptext.draw("This design may become visible to other players", midtop = T(640, 110),
		color = "#aabbff", shade = 1,
		fontsize = T(50), fontname = "ChelaOne", shadow = (1, 1), alpha = self.a
	)
	ptext.draw("Your name", midtop = T(240, 240),
		color = "#ffffff", shade = 1,
		fontsize = T(50), fontname = "GermaniaOne", shadow = (1, 1), alpha = self.a
	)
	ptext.draw("This design will be credited to you in the gallery. You can use your PyWeek name, but you don't have to. You can also leave it blank to share anonymously.",
		midtop = T(240, 420), width = T(380),
		color = "#aabbff", shade = 1,
		fontsize = T(32), fontname = "ChelaOne", shadow = (1, 1), alpha = self.a
	)
	ptext.draw("Design name", midtop = T(pview.w0 - 240, 240),
		color = "#ffffff", shade = 1,
		fontsize = T(50), fontname = "GermaniaOne", shadow = (1, 1), alpha = self.a
	)
	ptext.draw("You can leave this blank to share without naming the design.",
		midtop = T(pview.w0 - 240, 420), width = T(380),
		color = "#aabbff", shade = 1,
		fontsize = T(32), fontname = "ChelaOne", shadow = (1, 1), alpha = self.a
	)
	for jbox, (box, name) in enumerate(self.boxes):
		alpha = int(32 * self.a * (2 if jbox == self.jbox else 1))
		pview.fill((200, 200, 255, alpha), T(box))
		text = {
			"yourname": settings.yourname,
			"designname": self.designname,
		}[name]
		if text:
			ptext.draw(text, center = T(box.center), width = T(box.width),
				fontsize = T(34), fontname = "ChelaOne",
				color = "#ffffaa", shade = 1, shadow = (1, 1), alpha = self.a)
		else:
			ptext.draw("click to enter name", center = T(box.center), width = T(box.width),
				fontsize = T(26), fontname = "ChelaOne",
				color = "#ffffaa", shade = 1, shadow = (1, 1), alpha = 0.5 * self.a)

	if self.a >= 1:
		for jbutton, button in enumerate(self.buttons):
			button.draw(lit = (jbutton == self.jbutton))
		


