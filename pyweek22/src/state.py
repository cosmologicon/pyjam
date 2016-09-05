drawables = []
colliders = []
mouseables = []
thinkers = []
buildables = []
shootables = []

groups = drawables, colliders, mouseables, thinkers, buildables, shootables

def reset():
	for group in groups:
		del group[:]

def updatealive():
	for group in groups:
		group[:] = [m for m in group if m.alive]

def removeobj(obj):
	temp = obj.alive
	obj.alive = False
	updatealive()
	obj.alive = temp



