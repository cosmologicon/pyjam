
current = None
def set(s = None):
	global current
	current = s
	if s is not None:
		current.init()

