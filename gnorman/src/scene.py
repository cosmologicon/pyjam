from . import menuscene, playscene

stack = []

def current():
	return stack[-1] if stack else None
def push(s):
	stack.append(s)
def pop():
	stack.pop()


