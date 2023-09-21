you = None
DMs = []

cost = {
	"engine": [5, 10, 20],
	"gravnet": [5, 10, 20],
}

def getcost(techname):
	if techlevel[techname] <= 0:
		return None
	if techlevel[techname] > len(cost[techname]):
		return None
	return cost[techname][techlevel[techname] - 1]

def upgrade(techname):
	global xp
	if techname == "drag":
		techlevel["drag"] = (techlevel["drag"] + 1) % 5
		return
	if techlevel[techname] > 0:
		xp -= cost[techname][techlevel[techname] - 1]
	techlevel[techname] += 1

