_stack = []

def push(scene):
	_stack.append(scene)

def top():
	return _stack[-1] if _stack else None


class Scene:
	def __init__(self):
		pass
	def think(self, dt, kdowns, kpressed):
		pass
	def draw(self):
		pass
