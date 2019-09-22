_stack = []

def push(sc):
	_stack.append(sc)
	sc.init()

def current():
	return _stack[-1] if _stack else None

# TODO: pop and swap operations
# TODO: define and call suspend and resume

class Scene():
	# Called when a scene is pushed onto the stack.
	def init(self):
		pass
	# Called every game update.
	def think(self, dt, kdowns, kpressed):
		pass
	# Called every screen update.
	def draw(self):
		pass

