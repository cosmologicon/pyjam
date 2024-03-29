_stack = []

def push(sc):
	_stack.append(sc)
	sc.init()

def pop():
	if _stack:
		del _stack[-1]

def set(sc):
	while _stack:
		pop()
	push(sc)

def current():
	return _stack[-1] if _stack else None

# TODO: pop and swap operations
# TODO: define and call suspend and resume

class Scene:
	def __init__(self):
		pass
	# Called when a scene is pushed onto the stack.
	def init(self):
		pass
	# Called every game update from main.py.
	def think(self, dt, kpressed, kdowns, mpos, mdown, mup):
		pass
	# Called every screen update from main.py.
	def draw(self):
		pass

