

# Speed of the balloon in game units
speed = 4

# Length of the string
stringlength = 5

# Number of times leveled up
level = 0
# Current number needed to advance
goal = 2
# Current number collected
score = 0

def collect():
	global level, goal, score, speed
	score += 1
	# TODO: play a sound on level up
	if score == goal:
		level += 1
		goal = 2 + 1 * level
		speed = 4 + level
		score = 0

def hurt():
	global level, goal, score
	score = 0



