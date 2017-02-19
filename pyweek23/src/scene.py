stack = []

def add(scene):
	scene.init()
	stack.append(scene)

def pop():
	stack.pop()

def quit():
	while stack:
		stack.pop()
