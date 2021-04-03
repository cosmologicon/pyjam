
data = {}

data["empty"] = {
	"rings": [],
	"spawners": [],
	"trees": [],
}

data["single"] = {'rings': [{'pH': (2, 0), 'rH': 1, 'jcolor': 0}], 'spawners': [{'pH': (-1, -2), 'spec': [(1, 0)], 'tspawn': 2}, {'pH': (-1, -1), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (-2, 2), 'spec': [(2, 0)], 'tspawn': 2}], 'trees': []}

data["overage"] = {'rings': [{'pH': (0, 0), 'rH': 1, 'jcolor': 0}, {'pH': (0, 3), 'rH': 1, 'jcolor': 0}, {'pH': (3, -3), 'rH': 1, 'jcolor': 0}, {'pH': (-3, 0), 'rH': 1, 'jcolor': 0}], 'spawners': [{'pH': (0, -4), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (-1, -4), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (0, -5), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (1, -5), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (-5, 5), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (-4, 5), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (-4, 4), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (-5, 4), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (4, 1), 'spec': [(4, 0)], 'tspawn': 2}, {'pH': (4, 0), 'spec': [(4, 0)], 'tspawn': 2}, {'pH': (5, 0), 'spec': [(4, 0)], 'tspawn': 2}, {'pH': (5, -1), 'spec': [(4, 0)], 'tspawn': 2}], 'trees': []}

data["beech2"] = {'rings': [{'pH': (0, 4), 'rH': 1, 'jcolor': 0}, {'pH': (0, -4), 'rH': 1, 'jcolor': 0}], 'spawners': [{'pH': (4, 1), 'spec': [(4, 0)], 'tspawn': 3}, {'pH': (-4, 5), 'spec': [(2, 0)], 'tspawn': 3}, {'pH': (4, -5), 'spec': [(5, 0)], 'tspawn': 3}, {'pH': (-4, -1), 'spec': [(1, 0)], 'tspawn': 3}, {'pH': (-3, -2), 'spec': [(0, 0)], 'tspawn': 3}, {'pH': (3, 2), 'spec': [(3, 0)], 'tspawn': 3}], 'trees': []}


data["double"] = {'rings': [{'pH': (-4, 2), 'rH': 1, 'jcolor': 0}, {'pH': (4, -2), 'rH': 1, 'jcolor': 1}], 'spawners': [{'pH': (0, 0), 'spec': [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1)], 'tspawn': 3}], 'trees': []}



data["triple"] = {'rings': [{'pH': (0, 4), 'rH': 1, 'jcolor': 0}, {'pH': (-4, 5), 'rH': 1, 'jcolor': 1}, {'pH': (4, 1), 'rH': 1, 'jcolor': 2}], 'spawners': [{'pH': (-2, -3), 'spec': [(5, 0), (0, 1), (1, 2)], 'tspawn': 2}, {'pH': (2, -5), 'spec': [(5, 2), (0, 1), (1, 0)], 'tspawn': 2}, {'pH': (0, -2), 'spec': [(1, 1), (3, 0), (5, 2)], 'tspawn': 2}], 'trees': []}

data["pine3"] = {'rings': [{'pH': (0, 3), 'rH': 1, 'jcolor': 1}, {'pH': (3, -3), 'rH': 1, 'jcolor': 0}, {'pH': (-3, 0), 'rH': 1, 'jcolor': 2}], 'spawners': [{'pH': (2, 0), 'spec': [(0, 0), (1, 2), (2, 1)], 'tspawn': 3}, {'pH': (-2, 2), 'spec': [(4, 1), (5, 0), (0, 2)], 'tspawn': 3}, {'pH': (0, -2), 'spec': [(2, 2), (3, 1), (4, 0)], 'tspawn': 3}], 'trees': []}


data["final0"] = {'rings': [{'pH': (-4, 8), 'rH': 1, 'jcolor': 1}, {'pH': (4, 4), 'rH': 1, 'jcolor': 2}, {'pH': (-8, 4), 'rH': 1, 'jcolor': 0}, {'pH': (-4, -4), 'rH': 1, 'jcolor': 2}, {'pH': (4, -8), 'rH': 1, 'jcolor': 1}, {'pH': (8, -4), 'rH': 1, 'jcolor': 0}], 'spawners': [{'pH': (0, 5), 'spec': [(2, 1), (4, 2), (0, 0)], 'tspawn': 3}, {'pH': (5, -5), 'spec': [(-2, 1), (0, 0), (2, 2)], 'tspawn': 3}, {'pH': (-5, 0), 'spec': [(-2, 1), (0, 0), (2, 2)], 'tspawn': 3}, {'pH': (-3, 3), 'spec': [(1, 0), (3, 1), (5, 2)], 'tspawn': 3}, {'pH': (3, 0), 'spec': [(3, 0), (5, 2), (1, 1)], 'tspawn': 3}, {'pH': (0, -3), 'spec': [(1, 2), (3, 0), (5, 1)], 'tspawn': 3}], 'trees': []}


data["final"] = {'rings': [{'pH': (0, -2), 'rH': 1, 'jcolor': 0}, {'pH': (2, 0), 'rH': 1, 'jcolor': 1}, {'pH': (-2, 2), 'rH': 1, 'jcolor': 2}, {'pH': (0, 5), 'rH': 1, 'jcolor': 1}, {'pH': (5, -5), 'rH': 1, 'jcolor': 1}, {'pH': (-5, 0), 'rH': 1, 'jcolor': 2}, {'pH': (6, 3), 'rH': 1, 'jcolor': 0}, {'pH': (9, -3), 'rH': 1, 'jcolor': 0}, {'pH': (3, -9), 'rH': 1, 'jcolor': 2}, {'pH': (-3, -6), 'rH': 1, 'jcolor': 1}, {'pH': (-9, 6), 'rH': 1, 'jcolor': 0}, {'pH': (-6, 9), 'rH': 1, 'jcolor': 2}], 'spawners': [{'pH': (0, -10), 'spec': [(5, 2), (0, 0), (1, 1)], 'tspawn': 3}, {'pH': (-10, 10), 'spec': [(1, 1), (2, 2), (3, 0)], 'tspawn': 3}, {'pH': (10, 0), 'spec': [(3, 1), (4, 0), (5, 2)], 'tspawn': 3}, {'pH': (-9, 2), 'spec': [(0, 1), (1, 2), (2, 0)], 'tspawn': 3}, {'pH': (-7, -2), 'spec': [(0, 1), (1, 2), (2, 0)], 'tspawn': 3}, {'pH': (-2, 9), 'spec': [(2, 1), (3, 2), (4, 0)], 'tspawn': 3}, {'pH': (2, 7), 'spec': [(2, 2), (3, 1), (4, 0)], 'tspawn': 3}, {'pH': (9, -7), 'spec': [(4, 1), (5, 0), (0, 2)], 'tspawn': 3}, {'pH': (7, -9), 'spec': [(4, 2), (5, 0), (0, 1)], 'tspawn': 3}, {'pH': (-2, -4), 'spec': [(-2, 0), (0, 2), (2, 1)], 'tspawn': 3}, {'pH': (2, -6), 'spec': [(-2, 1), (0, 0), (2, 2)], 'tspawn': 3}, {'pH': (6, -2), 'spec': [(-2, 0), (0, 1), (2, 2)], 'tspawn': 3}, {'pH': (4, 2), 'spec': [(-2, 0), (0, 2), (2, 1)], 'tspawn': 3}, {'pH': (-4, 6), 'spec': [(-2, 1), (0, 2), (2, 0)], 'tspawn': 3}, {'pH': (-6, 4), 'spec': [(-2, 2), (0, 1), (2, 0)], 'tspawn': 3}], 'trees': []}


R = {
	"single": 6,
	"overage": 9,
	"beech2": 9,
	"double": 9,
	"triple": 10,
	"pine3": 12.3,
	"final0": 14,
	"final": 17.4,
}

buttons = {
	"single": ["oak"],
	"overage": ["oak"],
	"beech2": ["beech"],
	"double": ["beech"],
	"triple": ["beech"],
	"pine3": ["pine"],
	"final0": ["oak", "beech", "pine"],
	"final": ["oak", "beech", "pine"],
}

unlocks = {
	"single": ["overage"],
}


dialog = {
	"empty": [
		"What is this, a copse for ants?!",
		"It needs to be at least... three times bigger!",
	],
	"single": [
		"You call this a copse? Let's get some oak trees in here!",
		"Use trees to direct the magical energy into the toadstool ring!",
	],
	"overage": [
		"It takes 3 streams of magical energy to charge a toadstool ring.",
		"Any more than that is wasted.",
	],
	"beech2": [
		"Beech trees also direct the flow of energy, but not the same way that oaks do.",
		"Learn the difference!",
	],
}

tutorial = {
	"single": [
		"Click on the OAK button, then click on the ground to plant an oak tree.",
		"Trees can't be planted next to each other.",
		"Click on a planted tree to swap its orientation.",
		"Right click to remove a tree.",
	],
	"overage": [
		"Redirect the energy so that 3 streams are going to each ring.",
	],
}




