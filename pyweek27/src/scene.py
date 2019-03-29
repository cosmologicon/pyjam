from . import pview

_stack = []

def push(scene, *args, depth=-999, **kw):
	_stack.insert(-depth, scene)
	if hasattr(scene, "init"):
		scene.init(*args, **kw)

def top(n=1):
	return _stack[-n] if len(_stack) >= n else None

def pop():
	return _stack.pop() if _stack else None


