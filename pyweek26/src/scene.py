stack = []
def push(scene, *args):
	stack.append(scene)
	if hasattr(scene, "init"):
		scene.init(*args)
def pop():
	if not stack: return
	stack.pop()
def swap(scene, *args):
	pop()
	push(scene, *args)
def top():
	return stack[-1] if stack else None
