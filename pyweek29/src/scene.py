stack = []

def push(s, *args, **kwargs):
	stack.append(s)
	if hasattr(s, "init"):
		s.init(*args, **kwargs)

def pop():
	if stack:
		stack.pop()

def top():
	return stack[-1] if stack else None

