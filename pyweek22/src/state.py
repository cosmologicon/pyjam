def updatealive():
	mouseables[:] = [m for m in mouseables if m.alive]
	colliders[:] = [m for m in colliders if m.alive]
	drawables[:] = [m for m in drawables if m.alive]
	thinkers[:] = [m for m in thinkers if m.alive]
	buildables[:] = [m for m in buildables if m.alive]

def removeobj(obj):
	temp = obj.alive
	obj.alive = False
	updatealive()
	obj.alive = temp
