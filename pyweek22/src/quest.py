from . import dialog, mechanics

def init():
	global quests
	quests = [
		IntroQuest(),
		InstructionsQuest(),
	]

def think(dt):
	for quest in quests:
		if quest.done:
			continue
		quest.think(dt)

class Quest(object):
	def __init__(self):
		self.t = 0
		self.tstep = 0
		self.jstep = 0
		self.done = False
	def think(self, dt):
		self.t += dt
		self.tstep += dt
	def advance(self):
		self.jstep += 1
		self.tstep = 0

class IntroQuest(Quest):
	def think(self, dt):
		Quest.think(self, dt)
		if self.jstep == 0:
			if dialog.tquiet > 1:
				dialog.play("intro0")
				self.advance()

class InstructionsQuest(Quest):
	def think(self, dt):
		from . import state
		Quest.think(self, dt)
		if state.levelname == 1 and self.jstep == 0:
			if dialog.tquiet > 3:
				dialog.showtip("Click on the Grow button to grow an organelle.")
			if state.cell.slots:
				self.advance()
		if state.levelname == 1 and self.jstep == 1:
			if dialog.tquiet > 3 and self.tstep > 2 + mechanics.Xthatch:
				dialog.showtip("Drag an organelle out of the cell to make a defensive antibody.")
			if len(state.buildables) > 1:
				self.advance()
		if state.levelname == 2 and self.jstep == 2:
			if dialog.tquiet > 3 and self.tstep > 2:
				dialog.showtip("Combine two organelles into a single antibody to create a larger antibody.")
			if any(obj.formula() == "XX" for obj in state.buildables):
				self.advance()
		if state.levelname == 3 and self.jstep == 3:
			if dialog.tquiet > 3 and self.tstep > 2:
				dialog.showtip("Different combinations of organelles produce antibodies with different behavior.")
			if any(obj.formula() == "XY" for obj in state.buildables):
				self.advance()


