import pygame
from . import view, ptext, img, state, mechanics, progress
from .util import F

cursor = None
buttons = []

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
				fontsize = F(34), center = rect.center)
		else:
			view.screen.fill((120, 60, 0), rect)
			view.screen.fill((60, 30, 0), rect.inflate(F(-8), F(-8)))
			ptext.draw(self.name, color = "white", shadow = (1, 1), scolor = "black",
				fontsize = F(26), center = rect.center)

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
			cost = "Cost: %dRNA" % costs[0]
			if costs[1]:
				cost += " + %dDNA" % costs[1]
			text = "\n".join([
				cost,
				"Each organelle of this type left within the cell " + powers,
			])
			ptext.draw(text, topright = F(842, 16), fontsize = F(21), width = F(140),
				color = "orange", shadow = (1, 1), alpha = self.alpha)
		elif isinstance(self.current, Button) and "combos" in self.current.name:
			ptext.draw("Click to view available organelle combinations",
				topright = F(842, 16), fontsize = F(28), width = F(140),
				color = "orange", shadow = (1, 1), alpha = self.alpha)
		else:
			flavor = self.current.flavors()
			for j, f in enumerate(reversed(flavor)):
				p = F(820 - 30 * j, 50)
				pygame.draw.circle(view.screen, (0, 0, 0), p, F(20))
				img.draw("organelle-" + f, p, radius = F(18))

			if flavor not in progress.learned:
				text = "This combination of organelles is not yet unlocked."
			else:
				text = mechanics.towerinfo.get(flavor, flavor)
			ptext.draw(text, topright = F(842, 100), fontsize = F(30),
				color = "yellow", shadow = (1, 1), alpha = self.alpha)

towerinfo = TowerInfo()



