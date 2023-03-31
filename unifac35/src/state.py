import pickle

# The grid without any lights or obstacles.
grid0 = None

you = None
lights = []
obstacles = []
goals = []
escape = None

turn = None
maxturn = None

def grabat(pH):
	if you.pH == pH:
		return you
	for obstacle in obstacles:
		if obstacle.pH == pH and obstacle.ready:
			return obstacle

def advanceturn():
	global turn
	turn += 1
	for obstacle in obstacles:
		obstacle.reset()
	for goal in list(goals):
		if you.canclaim(goal):
			you.claim(goal)

def won():
	return not goals and you.pH == escape

def lost():
	return turn > maxturn


def updategrid():
	grid0.reset()
	for obj in lights + obstacles:
		grid0.block(obj.pH)
	for light in lights:
		light.illuminate()

snapstack = []
def snapshot():
	state = you, lights, obstacles, goals, turn, maxturn
	obj = pickle.dumps(state)
	snapstack.append(obj)
def restore(state):
	global you, lights, obstacles, goals, turn, maxturn
	you, lights, obstacles, goals, turn, maxturn = state
	updategrid()

def canundo():
	return len(snapstack) > 1

def undo():
	snapstack.pop()
	restore(pickle.loads(snapstack[-1]))

def reset():
	del snapstack[1:]
	restore(pickle.loads(snapstack[0]))
	
	
