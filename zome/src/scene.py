stack = []
def push(s):
	s.init()
	stack.append(s)
def pop():
	return stack.pop() if stack else None
def top():
	return stack[-1] if stack else None
