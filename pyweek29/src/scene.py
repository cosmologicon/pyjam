stack = []

def push(s, *args, **kwargs):
	if hasattr(s, "init"):
		s.init(*args, **kwargs)
	stack.append(s)

def pop():
	if stack:
		stack.pop()

def top():
	return stack[-1] if stack else None

