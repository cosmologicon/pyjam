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
	nsteps = 10
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
				return "Each habitat requires certain resources to activate (upper left), and provides certain resources when activated (lower right). Chain habitats together in the right order to satisfy all the requirements."
		if self.step == 5:
			if not self.moved:
				return "Right drag or arrow keys or WASD to pan."
			elif not self.zoomed:
				return "Scroll wheel or 1 and 2 keys to zoom."
			return "Conduits cannot pass through rocks or other conduits. (Have you tried out the buttons on the left?)"
		if self.step == 6:
			if not self.moved:
				return "Right drag or arrow keys or WASD to pan."
			elif not self.zoomed:
				return "Scroll wheel or 1 and 2 keys to zoom."
			return "Resources can be routed through habitats that are activated, if there's not room to go around. Use the habitat in the rocks to get the triangle to the lower habitat."
		if self.step == 7:
			return "Habitats may require more than one resource, and may provide more than one resource. Each conduit can transfer only one of a single type of resource."
		if self.step == 8:
			if self.tstep < 15:
				return "See README.txt for more controls and settings."
			return "Pro tip: set the Met Demand and Claimed Supply to OFF when you're building out to new areas. It might help to switch back to DIM if you need to reroute something."
		if self.step == 9:
			return "You are now a tube placing expert. Press Esc to return to the menu."

class EasyQuest(Quest):
	nsteps = 11
	def __init__(self):
		Quest.__init__(self)
		self.load(1)
	def load(self, phase):
		if phase == 1:
			generate.ezphase1()
		if phase == 2:
			generate.ezphase2()
		if phase == 3:
			generate.ezphase3()
	def check(self):
		if self.step == 0:
			self.advance()

		if self.step == 1 and state.numunsupplied() < 6:
			self.advance()
		if self.step == 2 and state.allsupplied():
			sound.play("advance")
			self.advance()
			self.load(2)

		if self.step == 3 and state.numunsupplied() < 12:
			self.advance()
		if self.step == 4 and state.numunsupplied() < 6:
			self.advance()
		if self.step == 5 and state.allsupplied():
			sound.play("advance")
			self.advance()
			self.load(3)

		if self.step == 6 and state.numunsupplied() < 12:
			self.advance()
		if self.step == 7 and state.numunsupplied() < 8:
			self.advance()
		if self.step == 8 and state.numunsupplied() < 4:
			self.advance()
		if self.step == 9 and state.allsupplied():
			self.advance()
			sound.play("advance")

	def marquee(self):
		if self.tstep > 15:
			return
		if self.step == 1:
			return "Planet Hardscrabble, Class W marginally habitable. 10 billion hectares of windswept wasteland."
		if self.step == 2:
			return "Nothing grows here. Nothing lives here but 70 million inhabitants crammed into aging, spartan, domed habitats, cut off from one another by kilometers of tundra."
		if self.step == 3:
			return "Traveling from one habitat to another was miserable and dangerous. Only the truly motivated - or desperate - ever made the journey."
		if self.step == 4:
			return "But everything changed with a revolutionary new invention: the tube!"
		if self.step == 5:
			return "Our greatest engineers developed an easy-to-deploy high-speed conduit to share resources between the habitats."
		if self.step == 6:
			return "Getting resources from one place to another allowed rapid progress, with more habitats coming online every year!"
		if self.step == 7:
			return "But just as important as moving resources was moving people. With easy travel between habitats, our culture developed alongside our technology."
		if self.step == 8:
			return "And now, all thanks to the tube, I see bright things in the future for Planet Hardscrabble. Hey, we'll have to change that name!"
		if self.step == 10:
			return "What do you think about: Planet Tubetopia? Thank you for playing. Press Esc to quit."

class MediumQuest(EasyQuest):
	def load(self, phase):
		if phase == 1:
			generate.medphase1()
		if phase == 2:
			generate.medphase2()
		if phase == 3:
			generate.medphase3()

class HardQuest(EasyQuest):
	def load(self, phase):
		if phase == 1:
			generate.phase1()
		if phase == 2:
			generate.phase2()
		if phase == 3:
			generate.phase3()
	

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

