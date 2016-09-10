import pygame
from . import view, ptext, img, state, mechanics, progress
from .util import F

cursor = None
buttons = []
playspeed = 1

done = set()  # For instruction quest

class Button(object):
	def __init__(self, rect, name):
		self.rect = rect
		self.name = name
	def within(self, screenpos):
		return pygame.Rect(F(self.rect)).collidepoint(screenpos)
	def draw(self):
		rect = pygame.Rect(F(self.rect))
		if self.name.startswith("Grow"):
			text, flavor = self.name.split()
			pygame.draw.circle(view.screen, (0, 0, 0), rect.center, int(rect.width / 1.7))
			img.draw("organelle-" + flavor, rect.center, radius = int(rect.width / 1.8))
			color = "white" if state.canbuy(flavor) else "#444444"
			ptext.draw(text, color = color, shadow = (1, 1), scolor = "black",
				fontsize = F(30), center = rect.center, fontname = "SansitaOne")
		elif self.name == "speed":
			view.screen.fill((120, 60, 0), rect)
			view.screen.fill((60, 30, 0), rect.inflate(F(-8), F(-8)))
			ptext.draw("%sx" % playspeed, color = "white", shadow = (1, 1), scolor = "black",
				fontsize = F(28), center = rect.center, fontname = "SansitaOne", lineheight = 0.7)
		else:
			view.screen.fill((120, 60, 0), rect)
			view.screen.fill((60, 30, 0), rect.inflate(F(-8), F(-8)))
			ptext.draw(self.name, color = "white", shadow = (1, 1), scolor = "black",
				fontsize = F(22), center = rect.center, fontname = "SansitaOne", lineheight = 0.7)

class TowerInfo(object):
	def __init__(self):
		self.current = None
		self.target = None
		self.alpha = 0
	def think(self, dt):
		if self.target != self.current:
			if self.alpha > 0:
				self.alpha = max(0, self.alpha - 5 * dt)
			if self.alpha == 0:
				self.current = self.target
		elif self.current is not None:
			self.alpha = min(1, self.alpha + 5 * dt)
	def draw(self):
		if self.current is None:
			return
		if isinstance(self.current, Button) and self.current.name.startswith("Grow"):
			flavor = self.current.name[-1]
			costs = {
				"X": [mechanics.Xcost1, mechanics.Xcost2],
				"Y": [mechanics.Ycost1, mechanics.Ycost2],
				"Z": [mechanics.Zcost1, mechanics.Zcost2],
			}[flavor]
			powers = {
				"X": "reduces damage to the cell by 30%.",
				"Y": "reduces grow times by 50%.",
				"Z": "heals the cell over time.",
			}[flavor]
			cost = "Cost: %d RNA" % costs[0]
			if costs[1]:
				cost += " + %d DNA" % costs[1]
			text = "\n".join([
				cost,
				"Each organelle of this type left within the cell " + powers,
			])
			ptext.draw(text, topright = F(842, 16), fontsize = F(21), width = F(180),
				color = "orange", shadow = (1, 1), alpha = self.alpha,
				fontname = "PatrickHand", lineheight = 0.8)
		elif isinstance(self.current, Button) and "combos" in self.current.name:
			ptext.draw("Click to view available organelle combinations",
				topright = F(842, 16), fontsize = F(28), width = F(140),
				color = "orange", shadow = (1, 1), alpha = self.alpha,
				fontname = "PatrickHand", lineheight = 0.8)
		elif isinstance(self.current, Button) and "Eject" in self.current.name:
			ptext.draw("Click to eject all organelles that are done growing from the cell.",
				topright = F(842, 16), fontsize = F(28), width = F(140),
				color = "orange", shadow = (1, 1), alpha = self.alpha,
				fontname = "PatrickHand", lineheight = 0.8)
		elif isinstance(self.current, Button):
			pass
		else:
			flavor = self.current.flavors()
			for j, f in enumerate(reversed(flavor)):
				p = F(820 - 30 * j, 50)
				pygame.draw.circle(view.screen, (0, 0, 0), p, F(20))
				img.draw("organelle-" + f, p, radius = F(18))
			if self.current.disabled:
				ptext.draw("INFECTED", center = F(760, 50), angle = 10, color = "#FF7F7F",
					owidth = 1, fontsize = F(26), fontname = "PatrickHand")

			if flavor not in progress.learned:
				text = "This combination of organelles is not yet unlocked."
			else:
				text = mechanics.towerinfo.get(flavor, flavor)
			if len(flavor) > 1:
				text += "\nRight click or Ctrl-click to split antibody."

			ptext.draw(text, topright = F(842, 75), fontsize = F(22),
				color = "yellow", shadow = (1, 1), alpha = self.alpha,
				fontname = "PatrickHand", lineheight = 0.8)

towerinfo = TowerInfo()

def reset():
	global buttons
	
	buttons = [
		Button((754, 380, 80, 80), "Pause"),
		Button((754, 290, 80, 80), "speed"),
	]
	if len(progress.learned) > 1:
		buttons.append(Button((120, 26, 80, 80), "Eject\nall"))
		buttons.append(Button((754, 200, 80, 80), "See\ncombos"))
	for j, flavor in enumerate("XYZ"):
		if flavor not in progress.learned:
			continue
		buttons.append(Button((26, 26 + 100 * j, 80, 80), "Grow " + flavor))


