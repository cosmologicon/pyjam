stack = []

def push(scene):
	stack.append(scene)
	if hasattr(scene, "onpush"):
		scene.onpush()

def top():
	return stack[-1] if stack else None

def pop():
	if not stack:
		return None
	scene = stack.pop()
	if hasattr(scene, "onpop"):
		scene.onpop()
	return scene

def swap(scene):
	pop()
	push(scene)


