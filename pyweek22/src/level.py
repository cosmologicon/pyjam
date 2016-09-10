# The levels that are unlocked when you beat a given level.

unlocks = {
	1: [2],
	2: [3],
	3: [4],
	4: [5],
	5: [6],
	6: [7, "endless"],
	7: [8],
	8: [9],
}

learns = {
	1: ["XX"],
	2: ["Y", "XY"],
	3: ["YY", "XXX", "XXY", "XYY"],
	4: ["YYY", "Z"],
	5: ["XZ", "YZ", "ZZ"],
	6: ["XXZ", "YYZ"],
	7: ["XZZ", "YZZ"],
	8: ["XYZ"],
}

slots = {
	1: 3,
	2: 3,
	3: 4,
	4: 5,
	5: 6,
	6: 7,
	7: 7,
	8: 7,
	9: 7,
}

def whenlearned(flavor):
	if flavor == "X":
		return 0
	for l, flavors in learns.items():
		if flavor in flavors:
			return l + 1
	return None

# position of each level on the menu screen
layout = {
	1: [30, 120, 70],
	2: [30, 320, 140],
	3: [45, 600, 200],
	4: [30, 400, 260],
	5: [30, 140, 220],
	6: [45, 220, 360],
	7: [30, 380, 400],
	8: [30, 520, 350],
	9: [50, 730, 380],
	"endless": [30, 70, 400],
	"qwin": [30, 800, 200],
}

# Level data

data = {
	1: {
		"Rlevel": 150,
		"cellpos": (0, -100),
		"health": 10,
		"atp": [20, 0],
		"autoatp": [0.2, 0],  # per second
		"wavespecs": [
			(12, 0, "ant", 3),
			(40, 0.15, "ant", 5),
			(60, -0.15, "ant", 10),
			(80, -0.1, "ant", 20),
			(80, 0.1, "ant", 20),
		],
	},
	2: {
		"Rlevel": 180,
		"cellpos": (-100, -100),
		"health": 20,
		"atp": [30, 0],
		"autoatp": [0.2, 0],
		"wavespecs": [
			(12, 0.2, "ant", 5),
			(30, 0.125, "ant", 10),
			(30, 0.125, "Lant", 2),
			(70, 0, "ant", 5),
			(70, 0, "Lant", 4),
			(120, 0.05, "ant", 5),
			(120, 0.05, "Lant", 6),
			(120, 0.2, "ant", 5),
			(120, 0.2, "Lant", 6),
		],
	},
	3: {
		"Rlevel": 250,
		"cellpos": (0, 0),
		"health": 40,
		"atp": [60, 0],
		"wavespecs": [
		],
		"streamspecs": [
			(20, "ant", 20, 0.1),
			(60, "Lant", 5, 0.05),
		],
	},
	4: {
		"Rlevel": 200,
		"cellpos": (-50, 140),
		"health": 50,
		"atp": [30, 0],
		"autoatp": [0.2, 0],
		"wavespecs": [
			(30, 0.4, "ant", 5),
			(30, 0.4, "flea", 2),
			(70, 0.5, "ant", 10),
			(70, 0.5, "flea", 4),
			(120, 0.35, "ant", 10),
			(120, 0.35, "flea", 4),
			(120, 0.55, "ant", 10),
			(120, 0.55, "flea", 4),
			(200, 0.45, "ant", 60),
			(200, 0.45, "flea", 20),
		],
	},
	5: {
		"Rlevel": 180,
		"cellpos": (150, 0),
		"health": 50,
		"atp": [30, 5],
		"autoatp": [0.2, 0],
		"wavespecs": [
			(25, 0.75, "ant", 5),
			(25, 0.75, "bee", 2),
			(60, 0.7, "ant", 5),
			(60, 0.8, "ant", 5),
			(60, 0.7, "bee", 5),
			(60, 0.8, "bee", 5),
			(120, 0.75, "ant", 30),
			(120, 0.75, "bee", 20),
			(200, 0.8, "bee", 15),
			(205, 0.75, "bee", 15),
			(205, 0.75, "Lbee", 5),
			(210, 0.7, "bee", 15),
		],
	},
	6: {
		"Rlevel": 300,
		"cellpos": (0, 0),
		"health": 100,
		"atp": [100, 15],
		"wavespecs": [
		],
		"streamspecs": [
			(20, "ant", 100, 0.2),
			(60, "Lant", 5, 0.05),
			(80, "bee", 10, 0.05),
		],
	},

	7: {
		"Rlevel": 250,
		"cellpos": (0, 0),
		"health": 100,
		"atp": [100, 15],
		"wavespecs": [
			(30, 0.25, "ant", 10),
			(33, 0.5, "ant", 15),
			(36, 0.75, "ant", 20),
			(39, 0, "ant", 25),
			(80, 0.25, "ant", 25),
			(83, 0.5, "ant", 25),
			(86, 0.75, "ant", 25),
			(89, 0, "ant", 25),
			(80, 0.25, "flea", 5),
			(83, 0.5, "flea", 5),
			(86, 0.75, "flea", 5),
			(89, 0, "flea", 5),
			(170, 0.1, "bee", 5),
			(173, 0.5, "bee", 5),
			(176, 0.9, "bee", 5),
			(178, 0.3, "bee", 5),
			(180, 0.7, "bee", 5),
			(170, 0.1, "flea", 5),
			(173, 0.5, "flea", 5),
			(176, 0.9, "flea", 5),
			(178, 0.3, "flea", 5),
			(180, 0.7, "flea", 5),
			(170, 0.1, "Lant", 5),
			(173, 0.5, "Lant", 5),
			(176, 0.9, "Lant", 5),
			(178, 0.3, "Lant", 5),
			(180, 0.7, "Lant", 5),
			(280, 0.1, "bee", 10),
			(280, 0.5, "bee", 10),
			(280, 0.9, "bee", 10),
			(280, 0.3, "bee", 10),
			(280, 0.7, "bee", 10),
			(280, 0.1, "flea", 10),
			(280, 0.5, "flea", 10),
			(280, 0.9, "flea", 10),
			(280, 0.3, "flea", 10),
			(280, 0.7, "flea", 10),
			(280, 0.1, "Lant", 10),
			(280, 0.5, "Lant", 10),
			(280, 0.9, "Lant", 10),
			(280, 0.3, "Lant", 10),
			(280, 0.7, "Lant", 10),
		],
	},

	8: {
		"Rlevel": 220,
		"cellpos": (0, -180),
		"health": 300,
		"atp": [10000000, 15],
		"wavespecs": [
			(20, 0, "ant", 30),
			(50, 0.15, "ant", 100),
			(50, 0.15, "Lant", 20),
			(50, 0.85, "ant", 100),
			(50, 0.85, "Lant", 20),
			(100, 0, "ant", 50),
			(100, 0, "Lant", 10),
			(100, 0, "bee", 50),
			(100, 0, "Lbee", 10),
			(150, 0.15, "bee", 100),
			(150, 0.15, "Lbee", 20),
			(150, 0.85, "bee", 100),
			(150, 0.85, "Lbee", 20),
			(200, 0, "flea", 50),
			(200, 0, "Lbee", 50),
			(200, 0, "Lant", 50),
		],
	},

	9: {
		"Rlevel": 350,
		"cellpos": (0, 0),
		"health": 500,
		"atp": [10000000, 10000000],
		"wavespecs": [
		],
		"streamspecs": [
			(20, "ant", 100, 0.1),
			(60, "Lant", 10, 0.1),
			(80, "bee", 30, 0.1),
			(100, "flea", 30, 0.1),
		],
	},



	# Endless mode
	"endless": {
		"Rlevel": 320,
		"cellpos": (0, 0),
		"health": 200,
		"atp": [10, 0],
		# Endless mode waves are procedurally generated after the first one.
		"wavespecs": [
			(0, 0, "endless", 1),
		],
	},

	# Quick-win level (just a single enemy)
	"qwin": {
		"Rlevel": 100,
		"cellpos": (0, -50),
		"health": 99999,
		"atp": 99999,
		"wavespecs": [
			(0, 0, 1),
		],
	},
}


