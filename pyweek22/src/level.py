# The levels that are unlocked when you beat a given level.

unlocks = {
	0: [1],
	1: [2],
}

# Level data

data = {
	0: {
		"Rlevel": 150,
		"cellpos": (0, -100),
		"health": 10,
		"atp": 20,
		"wavespecs": [
			(0, 0, 5),
			(20, 0.15, 10),
			(40, -0.15, 15),
			(60, -0.1, 20),
			(60, 0.1, 20),
		],
	},



	# Endless mode
	"endless": {
		"Rlevel": 400,
		"cellpos": (0, 0),
		"health": 100,
		"atp": 100,
		# Endless mode waves are procedurally generated after the first one.
		"wavespecs": [
			(0, 0, 5),
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


