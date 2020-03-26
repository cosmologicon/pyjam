
def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

def lepat(pos):
	return pickany(lep for lep in leps if (lep.x, lep.y) == pos)

def recharge():
	global leaps
	leaps = maxleaps

def rechargeleps():
	global jspin
	jspin = 0
	for lep in leps:
		lep.charged = True

def winning():
	return len(goals) >= ngoal and you.state == "grounded"

def beatcurrent():
	global ngoal
	ngoal = 0
	you.state = "grounded"

