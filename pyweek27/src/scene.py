from . import pview

_stack = []

def push(scene, *args, **kw):
	_stack.append(scene)
	if hasattr(scene, "init"):
		scene.init(*args, **kw)

def top():
	return _stack[-1] if _stack else None

def pop():
	return _stack.pop() if _stack else None


