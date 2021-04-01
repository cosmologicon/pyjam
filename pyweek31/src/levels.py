
data = {}

data["empty"] = {
	"rings": [],
	"spawners": [],
	"trees": [],
}

data["single"] = {'rings': [{'pH': (2, 0), 'rH': 1, 'jcolor': 0}], 'spawners': [{'pH': (-1, -2), 'spec': [(1, 0)], 'tspawn': 2}, {'pH': (-1, -1), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (-2, 2), 'spec': [(2, 0)], 'tspawn': 2}], 'trees': []}

data["overage"] = {'rings': [{'pH': (0, 0), 'rH': 1, 'jcolor': 0}, {'pH': (0, 3), 'rH': 1, 'jcolor': 0}, {'pH': (3, -3), 'rH': 1, 'jcolor': 0}, {'pH': (-3, 0), 'rH': 1, 'jcolor': 0}], 'spawners': [{'pH': (0, -4), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (-1, -4), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (0, -5), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (1, -5), 'spec': [(0, 0)], 'tspawn': 2}, {'pH': (-5, 5), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (-4, 5), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (-4, 4), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (-5, 4), 'spec': [(2, 0)], 'tspawn': 2}, {'pH': (4, 1), 'spec': [(4, 0)], 'tspawn': 2}, {'pH': (4, 0), 'spec': [(4, 0)], 'tspawn': 2}, {'pH': (5, 0), 'spec': [(4, 0)], 'tspawn': 2}, {'pH': (5, -1), 'spec': [(4, 0)], 'tspawn': 2}], 'trees': []}



data["triple"] = {'rings': [{'pH': (0, 4), 'rH': 1, 'jcolor': 0}, {'pH': (-4, 5), 'rH': 1, 'jcolor': 1}, {'pH': (4, 1), 'rH': 1, 'jcolor': 2}], 'spawners': [{'pH': (-2, -3), 'spec': [(5, 0), (0, 1), (1, 2)], 'tspawn': 2}, {'pH': (2, -5), 'spec': [(5, 2), (0, 1), (1, 0)], 'tspawn': 2}, {'pH': (0, -2), 'spec': [(1, 1), (3, 0), (5, 2)], 'tspawn': 2}], 'trees': []}


data["final"] = {'rings': [{'pH': (0, -2), 'rH': 1, 'jcolor': 0}, {'pH': (2, 0), 'rH': 1, 'jcolor': 1}, {'pH': (-2, 2), 'rH': 1, 'jcolor': 2}, {'pH': (0, 5), 'rH': 1, 'jcolor': 1}, {'pH': (5, -5), 'rH': 1, 'jcolor': 1}, {'pH': (-5, 0), 'rH': 1, 'jcolor': 2}, {'pH': (6, 3), 'rH': 1, 'jcolor': 0}, {'pH': (9, -3), 'rH': 1, 'jcolor': 0}, {'pH': (3, -9), 'rH': 1, 'jcolor': 2}, {'pH': (-3, -6), 'rH': 1, 'jcolor': 1}, {'pH': (-9, 6), 'rH': 1, 'jcolor': 0}, {'pH': (-6, 9), 'rH': 1, 'jcolor': 2}], 'spawners': [{'pH': (0, -10), 'spec': [(5, 2), (0, 0), (1, 1)], 'tspawn': 3}, {'pH': (-10, 10), 'spec': [(1, 1), (2, 2), (3, 0)], 'tspawn': 3}, {'pH': (10, 0), 'spec': [(3, 1), (4, 0), (5, 2)], 'tspawn': 3}, {'pH': (-9, 2), 'spec': [(0, 1), (1, 2), (2, 0)], 'tspawn': 3}, {'pH': (-7, -2), 'spec': [(0, 1), (1, 2), (2, 0)], 'tspawn': 3}, {'pH': (-2, 9), 'spec': [(2, 1), (3, 2), (4, 0)], 'tspawn': 3}, {'pH': (2, 7), 'spec': [(2, 2), (3, 1), (4, 0)], 'tspawn': 3}, {'pH': (9, -7), 'spec': [(4, 1), (5, 0), (0, 2)], 'tspawn': 3}, {'pH': (7, -9), 'spec': [(4, 2), (5, 0), (0, 1)], 'tspawn': 3}, {'pH': (-2, -4), 'spec': [(-2, 0), (0, 2), (2, 1)], 'tspawn': 3}, {'pH': (2, -6), 'spec': [(-2, 1), (0, 0), (2, 2)], 'tspawn': 3}, {'pH': (6, -2), 'spec': [(-2, 0), (0, 1), (2, 2)], 'tspawn': 3}, {'pH': (4, 2), 'spec': [(-2, 0), (0, 2), (2, 1)], 'tspawn': 3}, {'pH': (-4, 6), 'spec': [(-2, 1), (0, 2), (2, 0)], 'tspawn': 3}, {'pH': (-6, 4), 'spec': [(-2, 2), (0, 1), (2, 0)], 'tspawn': 3}], 'trees': []}


R = {
	"single": 6,
	"overage": 9,
	"final": 17.4,
}

unlocks = {
	"single": ["overage"],
}


dialog = {
	"empty": [
		"What is this, a copse for ants?!",
		"It needs to be at least... three times bigger!",
	],
}


