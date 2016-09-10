from . import dialog, mechanics

def init():
	global quests
	quests = [
		IntroQuest(),
		InstructionsQuest(),
		EndlessQuest(),
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
		from . import state
		Quest.think(self, dt)
		if state.levelname in range(1, 10):
			if dialog.tquiet > 1:
				dialog.play("C0%d" % state.levelname)
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
		if state.levelname == 1 and self.jstep == 2:
			if dialog.tquiet > 3 and self.tstep > 8:
				dialog.showtip("You can drag an antibody to reposition it.")
			if self.tstep > 16:
				self.advance()
		if state.levelname == 1 and self.jstep == 4:
			if dialog.tquiet > 3 and self.tstep > 8:
				dialog.showtip("Use the mouse wheel or the keys 1/2 to zoom.")
			if self.tstep > 16:
				self.advance()

		if state.levelname == 2 and self.jstep == 5:
			if dialog.tquiet > 3 and self.tstep > 2:
				dialog.showtip("Combine two organelles into a single antibody to create a larger antibody.")
			if any(len(obj.formula()) > 1 for obj in state.buildables):
				self.advance()

		if state.levelname == 3 and self.jstep == 6:
			if dialog.tquiet > 3 and self.tstep > 2:
				dialog.showtip("Different combinations of organelles produce antibodies with different behavior.")
			if any(obj.formula() == "XY" for obj in state.buildables) and self.tstep > 8:
				self.advance()
		if state.levelname == 3 and self.jstep == 7:
			if dialog.tquiet > 3 and self.tstep > 8:
				dialog.showtip("Defeat the large virus quickly before you're overwhelmed.")
			if self.tstep > 16:
				self.advance()


class EndlessQuest(Quest):
	def think(self, dt):
		from . import state
		Quest.think(self, dt)
		if self.jstep == 0 and state.levelname == "endless" and len(state.donewaves) > 50 and dialog.tquiet > 2:
			self.advance()
		if self.jstep == 1:
			from . import progress
			dialog.showtip("Mega-bomb antibody unlocked!")
			progress.learned.add("ZZZ")
			progress.save()
			if self.tstep > 3:
				self.advance()


