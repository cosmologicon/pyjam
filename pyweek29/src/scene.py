stack = []

def push(s):
	if hasattr(s, "init"):
		s.init()
	stack.append(s)

def pop():
	if stack:
		stack.pop()

def top():
	return stack[-1] if stack else None

