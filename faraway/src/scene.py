# Module that just keeps track of the current scene.

current = None
def set(s = None):
	global current
	current = s
	if s is not None:
		current.init()

