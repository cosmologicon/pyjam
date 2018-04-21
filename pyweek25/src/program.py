import random
from . import state, pathfind, progress

# Whether the part with the given tag has been claimed
def tagclaimed(tag):
	return state.tags[tag] not in state.parts
def attag(who, tag):
	return state.tags[tag] == state.pieces[who].xyG()

def gettargettags():
	if progress.current == "act1.level1":
		for tag in "abecd":
			if not tagclaimed(tag):
				return [tag]
		return [None]
	if progress.current == "act1.level3":
		for step, tag in enumerate("dba"):
			if state.AIstep == step:
				if attag("Y", tag):
					state.AIstep += 1
					return gettargettags()
				return [tag]
		return ["a"]
	if progress.current == "act1.level5":
		for tag in "abcd":
			if not tagclaimed(tag):
				return [tag]
		return [None]

def randommove():
	for cell in state.neighbors(state.pieces["Y"].xyG()):
		if state.canclaimpart("Y", cell) or state.canclaimtile("Y", cell) or state.canmoveto("Y", cell):
			return cell
	return state.pieces["Y"].xyG()

def move():
	for target in list(gettargettags()) + [None]:
		if target is None:
			return randommove()
		else:
			step = pathfind.find(state.pieces["Y"], state.tags[target])
			if step is None:
				continue
			_, p = step
			if p is None:
				continue
			return p
	return randommove()


