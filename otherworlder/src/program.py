import random
from . import state, pathfind, progress

# Whether the part with the given tag has been claimed
def tagclaimed(tag):
	return state.tags[tag] not in state.parts
def attag(who, tag):
	return state.tags[tag] == state.pieces[who].xyG()

def gettargettags():
	def seekandstep(who, tag):
		if attag(who, tag):
			state.AIstep += 1
			return gettargettags()
		return [tag]

	if progress.current == "act1.level1":
		for tag in "abecd":
			if not tagclaimed(tag):
				return [tag]
	if progress.current == "act1.level2":
		if state.AIstep == 0:
			state.AIstep = random.choice(["abcdefg", "abcedfg"])
		for tag in state.AIstep:
			if not tagclaimed(tag):
				return [tag]
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
	if progress.current == "act2.level1":
		if state.AIstep == 0:
			return seekandstep("X", "j")
		if state.AIstep == 1:
			for tag in "aeb":
				if not tagclaimed(tag):
					return [tag]
			return seekandstep("X", "k")
		if state.AIstep == 2:
			for tag in "cd":
				if not tagclaimed(tag):
					return [tag]
	if progress.current == "act2.level2":
		toget = "abcdefg" if state.scores["X"] == 0 else "acdefg"
		for tag in toget:
			if not tagclaimed(tag):
				return [tag]
	if progress.current == "act2.level3":
		for tag in "ab":
			if not tagclaimed(tag):
				return [tag]
	if progress.current == "act2.level5":
		if state.AIstep == 0:
			for tag in "fgea":
				if not tagclaimed(tag):
					return [tag]
			state.AIstep += 1
		if state.AIstep == 1:
			if tagclaimed("d"):
				state.AIstep += 1
			else:
				return seekandstep("X", "h")
		if state.AIstep == 2:
			for tag in "dbc":
				if not tagclaimed(tag):
					return [tag]
			state.AIstep += 1
	return [None]


def randommove():
	who = "Y" if progress.current.startswith("act1") else "X"
	for cell in state.neighbors(state.pieces[who].xyG()):
		if state.canclaimpart(who, cell) or state.canclaimtile(who, cell) or state.canmoveto(who, cell):
			return cell
	return state.pieces[who].xyG()

def move():
	who = "Y" if progress.current.startswith("act1") else "X"
	for target in list(gettargettags()) + [None]:
		if target is None:
			return randommove()
		else:
			step = pathfind.find(state.pieces[who], state.tags[target])
			if step is None:
				continue
			_, p = step
			if p is None:
				continue
			return p
	return randommove()


