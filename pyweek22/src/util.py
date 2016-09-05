import os.path, os

f = 1
def F(x, *args):
	if args:
		return F([x] + list(args))
	if isinstance(x, (list, tuple)):
		return [F(a) for a in x]
	return max(int(x * f), 1) if x > 0 else int(x * f)

def mkdir(filename):
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))

