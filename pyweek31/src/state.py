

bugs = []
trees = []

def treeat(pH):
	for tree in trees:
		if tree.pH == pH:
			return tree
	return None


