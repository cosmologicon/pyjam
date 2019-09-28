# The module is called "quest", but really anything that involves progress can be a quest, including
# tutorials and instructions. This is basically a dumping ground for detailed progression we don't
# want to put anywhere else.

from . import dialog, state, view

# List of currently active quests
active = []

def start(q):
	q.start()
	active.append(q)

def think(dt):
	for q in active:
		q.think(dt)
	active[:] = [q for q in active if not q.done]


class Quest:
	def start(self):
		self.done = False
		self.step = 0
		self.t = 0  # Time spent in current step
	def think(self, dt):
		self.t += dt
	def advance(self):
		self.step += 1
		self.t = 0

class FixQuest(Quest):
	def __init__(self):
		Quest.__init__(self)
		self.car = None
	def think(self, dt):
		Quest.think(self, dt)
		if self.car is not None:
			for car in state.cars:
				if car is not self.car:
					car.broken = False
		if self.step == 0:
			if any(car.broken for car in state.cars):
				self.car = [car for car in state.cars if car.broken][0]
				self.advance()
		if self.step == 1:
			if not self.car.broken:
				dialog.helptext()
				self.done = True
			elif self.t > 0.3:
				if self.car is state.currentcar():
					dialog.helptext("It won't run at full speed like that. Give it a few good whacks.")
				else:
					dialog.helptext("Uh-oh! Looks like one of the cars is on the fritz. Click on the flashing car on the map.")

class TutorialQuest(Quest):
	def __init__(self):
		Quest.__init__(self)
		self.mission = state.missionstacks["Skyburg"][0]
	def think(self, dt):
		Quest.think(self, dt)
		if self.step == 0:
			if any(target.name == "Skyburg" for station in state.stations for pop in station.held for target in pop.htargets):
				dialog.helptext()
				self.advance()
			elif self.t > 0.3:
				if view.zW0 > 0:
					dialog.helptext("Click on Ground Control station on the map to the right.")
				else:
					dialog.helptext("Click on a Workazoid and drag them to Skyburg station to reassign.")
		if self.step == 1:
			if not any(pop.wantscar() for station in state.stations for pop in station.held):
				dialog.helptext()
				self.advance()
			elif self.t > 0.3:
				s = state.currentstation()
				if s and s.name == "Skyburg":
					dialog.helptext("Open the port on the N side of the station.")
				else:
					dialog.helptext("The Workazoid is assigned but doesn't have any way to reach the station. Click on Skyburg station on the map to the right.")
		if self.step == 2:
			if any(station.name == "Skyburg" and station.held for station in state.stations):
				dialog.helptext()
				self.advance()
			elif self.t > 0.3:
				dialog.helptext("Now just wait for the car to bring the Workazoid. You can click on the car to follow it.")
		if self.step == 3:
			if self.t > 0.3:
				dialog.helptext("Moving crew members to stations lets you complete tasks at that station, and keep more ports open. Click on the Complete Mission button to claim the reward!")
		if self.mission not in state.missionstacks["Skyburg"]:
			self.done = True
			dialog.helptext()

class ChatQuest(Quest):
	def think(self, dt):
		if self.step == 0 and state.progress.missions >= 3:
			dialog.startconvo("chat1")
			self.advance()
		if self.step == 1 and state.progress.missions >= 8:
			dialog.startconvo("chat2")
			self.advance()
		if self.step == 2 and state.progress.missions >= 13:
			dialog.startconvo("chat3")
			self.advance()
		if self.step == 3 and state.progress.done:
			dialog.startconvo("end")
			self.done = True

class TestQuest(Quest):
	def think(self, dt):
		Quest.think(self, dt)
		if self.step == 0 and self.t > 0.3:
			dialog.run("Want a quest, huh? Visit the Northeast side of Skyburg.")
			self.advance()
		if self.step == 1:
			s = state.currentstation()
			if s and s.name == "Skyburg" and view.dA(view.A, 1) == 0:
				dialog.run("Congratulations. You finished a quest. Want a reward? Tough, we haven't implemented it yet!")
				self.advance()
				self.done = True

class ReallocateQuest(Quest):
	def think(self, dt):
		Quest.think(self, dt)
		if self.step == 0 and self.t > 0.3:
			dialog.run("Quest: reassign one worker from Counterweight to each of the other four stations. All stations must have a worker at the same time to complete the quest.")
			self.advance()
		if self.step == 1:
			if all(s.held for s in state.stations):
				dialog.run("Congratulations. You finished a quest. Want a reward? Tough, we haven't implemented it yet!")
				self.advance()
				self.done = True

class MissionQuest(Quest):
	def __init__(self, station, need, reward):
		self.station = station
		self.need = need
		self.reward = reward
		self.tdone = 0
	def fulfilled(self):
		pnames = [held.name for held in self.station.held]
		return all(pnames.count(name) >= self.need.count(name) for name in set(self.need))
	def think(self, dt):
		if self.fulfilled():
			self.tdone += dt
		else:
			self.tdone = 0
	def finish(self):
		self.advance()
		self.done = True
		text = state.completemission(self.reward)
		dialog.run("Mission Complete\n" + text)
		self.station.mission = None
		state.updatemissions()

