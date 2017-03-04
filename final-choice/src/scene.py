stack = []

def push(scene, *args, **kw):
	scene.init(*args, **kw)
	stack.append(scene)

def pop():
	stack.pop()

def quit():
	while stack:
		stack.pop()
