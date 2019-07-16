
_stack = []

def push(scene):
	_stack.append(scene)
	if hasattr(scene, "init"):
		scene.init()

def pop():
	del _stack[-1]

def top():
	return _stack[-1] if _stack else None

