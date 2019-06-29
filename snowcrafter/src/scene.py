from __future__ import division
from . import pview

_stack = []

def push(scene, *args, **kw):
	depth = -999
	if "depth" in kw:
		depth = kw["depth"]
		del kw["depth"]
	_stack.insert(-depth, scene)
	if hasattr(scene, "init"):
		scene.init(*args, **kw)

def top(n=1):
	return _stack[-n] if len(_stack) >= n else None

def pop():
	return _stack.pop() if _stack else None


