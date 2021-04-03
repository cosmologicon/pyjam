
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


data["oakpine"] = {'rings': [{'pH': (-3, 4), 'rH': 1, 'jcolor': 1}, {'pH': (0, 5), 'rH': 1, 'jcolor': 0}, {'pH': (3, 1), 'rH': 1, 'jcolor': 2}], 'spawners': [{'pH': (-1, -1), 'spec': [(0, 1), (2, 0), (4, 2)], 'tspawn': 3}, {'pH': (0, 0), 'spec': [(0, 0), (2, 2), (4, 1)], 'tspawn': 3}, {'pH': (1, -2), 'spec': [(0, 2), (2, 1), (4, 0)], 'tspawn': 3}], 'trees': []}



data["final0"] = {'rings': [{'pH': (-4, 8), 'rH': 1, 'jcolor': 1}, {'pH': (4, 4), 'rH': 1, 'jcolor': 2}, {'pH': (-8, 4), 'rH': 1, 'jcolor': 0}, {'pH': (-4, -4), 'rH': 1, 'jcolor': 2}, {'pH': (4, -8), 'rH': 1, 'jcolor': 1}, {'pH': (8, -4), 'rH': 1, 'jcolor': 0}], 'spawners': [{'pH': (0, 5), 'spec': [(2, 1), (4, 2), (0, 0)], 'tspawn': 3}, {'pH': (5, -5), 'spec': [(-2, 1), (0, 0), (2, 2)], 'tspawn': 3}, {'pH': (-5, 0), 'spec': [(-2, 1), (0, 0), (2, 2)], 'tspawn': 3}, {'pH': (-3, 3), 'spec': [(1, 0), (3, 1), (5, 2)], 'tspawn': 3}, {'pH': (3, 0), 'spec': [(3, 0), (5, 2), (1, 1)], 'tspawn': 3}, {'pH': (0, -3), 'spec': [(1, 2), (3, 0), (5, 1)], 'tspawn': 3}], 'trees': []}


data["final1"] = {'rings': [{'pH': (0, -2), 'rH': 1, 'jcolor': 0}, {'pH': (2, 0), 'rH': 1, 'jcolor': 1}, {'pH': (-2, 2), 'rH': 1, 'jcolor': 2}, {'pH': (0, 5), 'rH': 1, 'jcolor': 1}, {'pH': (5, -5), 'rH': 1, 'jcolor': 1}, {'pH': (-5, 0), 'rH': 1, 'jcolor': 2}, {'pH': (6, 3), 'rH': 1, 'jcolor': 0}, {'pH': (9, -3), 'rH': 1, 'jcolor': 0}, {'pH': (3, -9), 'rH': 1, 'jcolor': 2}, {'pH': (-3, -6), 'rH': 1, 'jcolor': 1}, {'pH': (-9, 6), 'rH': 1, 'jcolor': 0}, {'pH': (-6, 9), 'rH': 1, 'jcolor': 2}], 'spawners': [{'pH': (0, -10), 'spec': [(5, 2), (0, 0), (1, 1)], 'tspawn': 3}, {'pH': (-10, 10), 'spec': [(1, 1), (2, 2), (3, 0)], 'tspawn': 3}, {'pH': (10, 0), 'spec': [(3, 1), (4, 0), (5, 2)], 'tspawn': 3}, {'pH': (-9, 2), 'spec': [(0, 1), (1, 2), (2, 0)], 'tspawn': 3}, {'pH': (-7, -2), 'spec': [(0, 1), (1, 2), (2, 0)], 'tspawn': 3}, {'pH': (-2, 9), 'spec': [(2, 1), (3, 2), (4, 0)], 'tspawn': 3}, {'pH': (2, 7), 'spec': [(2, 2), (3, 1), (4, 0)], 'tspawn': 3}, {'pH': (9, -7), 'spec': [(4, 1), (5, 0), (0, 2)], 'tspawn': 3}, {'pH': (7, -9), 'spec': [(4, 2), (5, 0), (0, 1)], 'tspawn': 3}, {'pH': (-2, -4), 'spec': [(-2, 0), (0, 2), (2, 1)], 'tspawn': 3}, {'pH': (2, -6), 'spec': [(-2, 1), (0, 0), (2, 2)], 'tspawn': 3}, {'pH': (6, -2), 'spec': [(-2, 0), (0, 1), (2, 2)], 'tspawn': 3}, {'pH': (4, 2), 'spec': [(-2, 0), (0, 2), (2, 1)], 'tspawn': 3}, {'pH': (-4, 6), 'spec': [(-2, 1), (0, 2), (2, 0)], 'tspawn': 3}, {'pH': (-6, 4), 'spec': [(-2, 2), (0, 1), (2, 0)], 'tspawn': 3}], 'trees': []}


R = {
	"empty": 17.4,
	"single": 6,
	"overage": 9,
	"beech2": 9,
	"double": 9,
	"triple": 10,
	"pine3": 12.3,
	"oakpine": 10.5,
	"final0": 14,
	"final1": 17.4,
}

buttons = {
	"single": ["oak"],
	"overage": ["oak"],
	"beech2": ["beech"],
	"double": ["beech"],
	"triple": ["oak", "beech"],
	"pine3": ["pine"],
	"oakpine": ["oak", "pine"],
	"final0": ["oak", "beech", "pine"],
	"final1": ["oak", "beech", "pine"],
}

unlocks = {
	"single": ["overage"],
	"overage": ["beech2"],
	"beech2": ["double"],
	"double": ["triple"],
	"triple": ["pine3"],
	"pine3": ["oakpine"],
	"oakpine": ["beechpine"],
	"beechpine": ["final0"],
	"final0": ["final1"],
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
	"final0": [
		"You've helped all the gnomes build their copses!",
		"Just one more to go: mine!",
	],
	"final1": [
		"And the gnomes lived happily ever after! The end!",
		"Thanks for playing Gnorman's Copse!",
		"Goodbye!",
		"Oh, you're still here?",
		"Okay, here's an optional bonus stage. Make a copse for yourself!",
	],
}

tutorial = {
	"single": [
		"Click on the OAK button, then click on the ground to plant an oak tree.",
		"Trees can't be planted next to each other.",
		"Click on a planted tree to swap its orientation.",
		"Right click to remove a tree.",
		"Click on a flower to highlight its stream. Click again to disable.",
		"Direct all three streams into the ring at the same time!",
	],
	"overage": [
		"Redirect the energy so that 3 streams are going to each ring.",
	],
	"final1": [
		"Thank you for playing!",
	],
}




