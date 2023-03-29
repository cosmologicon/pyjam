
# The grid without any lights or obstacles.
grid0 = None

# The updated grid with lights and obstacles in place.
grid = None

you = None
lights = []
obstacles = []
goals = []

turn = None
maxturn = None

def grabat(pH):
	if you.pH == pH:
		return you
	for obstacle in obstacles:
		if obstacle.pH == pH:
			return obstacle


