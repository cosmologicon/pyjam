

def cycle(value, values, reverse = False):
	values = list(values)
	if reverse:
		oks = [v for v in values if v < value]
		return max(oks or values)
	else:
		oks = [v for v in values if v > value]
		return min(oks or values)

