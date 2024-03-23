from . import state, generate, view, sound

class Quest:
	nsteps = 1
	def __init__(self):
		self.t = 0
		self.step = 0
		self.done = False
		self.tstep = 0
	def think(self, dt):
		self.t += dt
		self.tstep += dt
		self.check()
	def check(self):
		pass
	def marquee(self):
		return None
	def advance(self):
		self.step += 1
		self.tstep = 0
		if self.step >= self.nsteps:
			self.done = True


class TutorialQuest(Quest):
	nsteps = 9
	def __init__(self):
		Quest.__init__(self)
		view.VscaleG = 120
		view.xG0, view.yG0 = 0, 0
		generate.tutorial1()
		self.moved = False
		self.zoomed = False
		self.pG0 = None
		self.zoom = None
	def check(self):
		from . import playscene
		building = playscene.building
		if self.pG0 is None:
			self.pG0 = view.xG0, view.yG0
		if self.zoom is None:
			self.zoom = view.VscaleG
		if self.pG0 is not None and self.pG0 != (view.xG0, view.yG0):
			self.moved = True
		if self.zoom is not None and self.zoom != view.VscaleG:
			self.zoomed = True
		if self.step == 0:
			self.advance()
		if self.step == 1 and building:
			self.advance()
		if self.step == 2 and building and len(building.pHs) > 1:
			self.advance()
		if self.step == 3 and state.allsupplied():
			self.advance()
			sound.play("advance")
			generate.tutorial2()
		if self.step == 4 and state.allsupplied():
			self.advance()
			sound.play("advance")
			generate.tutorial3()
		if self.step == 5 and sum(not planet.supplied for planet in state.planets) <= 1:
			self.advance()
		if self.step == 6 and state.allsupplied():
			self.advance()
			sound.play("advance")
			generate.tutorial4()
		if self.step == 7 and state.allsupplied():
			self.advance()
			sound.play("advance")
			generate.tutorial5()
		if self.step == 8 and state.allsupplied():
			sound.play("win")
			self.advance()
	def marquee(self):
		if self.step == 1:
			return "Click on the western habitat."	
		if self.step == 2:
			return "Click or drag on adjacent spaces to build a conduit."
		if self.step == 3:
			if not state.tubes:
				return "Right click to cancel. Build a conduit from the western habitat to the eastern habitat."
			else:
				return "Reverse or remove a conduit once it's built by selecting it and using the buttons in the lower left."
		if self.step == 4:
			if not self.moved:
				return "Right drag or arrow keys or WASD to pan."
			elif not self.zoomed:
				return "Scroll wheel or 1 and 2 keys to zoom."
			elif sum(planet.supplied for planet in state.planets) < 3:
				return "Each habitat requires certain resources to activate, and provides certain resources when activated. Chain habitats together in the right order to satisfy all the requirements."
		if self.step == 5:
			if not self.moved:
				return "Right drag or arrow keys or WASD to pan."
			elif not self.zoomed:
				return "Scroll wheel or 1 and 2 keys to zoom."
			return "Conduits cannot pass through rocks or other conduits."
		if self.step == 6:
			if not self.moved:
				return "Right drag or arrow keys or WASD to pan."
			elif not self.zoomed:
				return "Scroll wheel or 1 and 2 keys to zoom."
			return "Resources can be routed through activated habitats, if there's not room to go around."
		if self.step == 7:
			return "Habitats may require more than one resource, and may provide more than one resource. Each conduit can transfer only one of a single type of resource."
		if self.step == 8:
			if self.tstep < 15:
				return "See README.txt for more controls and settings."
			return "Press Esc at any time to quit. Your progress is saved."

class EasyQuest(Quest):
	nsteps = 10
	def __init__(self):
		Quest.__init__(self)
		generate.ezphase1()
	def check(self):
		if self.step == 0:
			self.advance()
		if self.step == 1 and state.allsupplied():
			self.advance()
			sound.play("advance")
			generate.ezphase2()
		if self.step == 2 and state.allsupplied():
			self.advance()
			sound.play("advance")
			generate.ezphase3()
		if self.step == 3 and state.allsupplied():
			self.advance()
			sound.play("advance")
	def marquee(self):
		if self.tstep > 15:
			return
		if self.step == 1:
			return "Welcome to planet Hardscrabble. Dialog #1."
		if self.step == 2:
			return "Welcome to planet Hardscrabble. Dialog #2."
		if self.step == 3:
			return "Welcome to planet Hardscrabble. Dialog #3."
		if self.step == 4:
			return "Welcome to planet Hardscrabble. Dialog #4."
		if self.step == 5:
			return "Welcome to planet Hardscrabble. Dialog #5."
		if self.step == 6:
			return "Welcome to planet Hardscrabble. Dialog #6."
		if self.step == 7:
			return "Welcome to planet Hardscrabble. Dialog #7."
		if self.step == 8:
			return "Welcome to planet Hardscrabble. Dialog #8."
		if self.step == 9:
			return "Welcome to planet Hardscrabble. Dialog #9."

class HardQuest(Quest):
	nsteps = 4
	def __init__(self):
		Quest.__init__(self)
		generate.phase1()
	def check(self):
		if self.step == 0:
			self.advance()
		if self.step == 1 and state.allsupplied():
			self.advance()
			generate.phase2()
		if self.step == 2 and state.allsupplied():
			self.advance()
			generate.phase3()
		if self.step == 3 and state.allsupplied():
			self.advance()
	

quests = []

def think(dt):
	global quests
	for q in quests:
		q.think(dt)
	quests = [q for q in quests if not q.done]

def marquee():
	for q in quests:
		if q.marquee():
			return q.marquee()

