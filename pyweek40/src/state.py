
costs = {
	"remove": 0,
	"segment": 1,
	"office": 10,
	"spire": 20,
	"residence1": 10,
	"vending1": 10,
	"residence2": 30,
	"vending2": 30,
	"residence3": 100,
	"vending3": 100,
}

unlocks = {
	"vending1": 1,
	"residence1": 2,
	"residence2": 4,
	"vending2": 4,
	"residence3": 5,
	"vending3": 5,
}

level = 0
maxheight = 0
maxheights = [5, 5, 6, 9, 12, 16]
growcosts = [30, 60, 100, 100, 200]
growcosts = [0, 0, 0, 0, 0, 0, 0]
growpops = [0, 2, 5, 10, 20, 30]
money = 30
maxmoneys = [30, 60, 100, 100, 200]
maxmoneys = [1000000] * 100
maxmoney = maxmoneys[0]
things = []


def init():
	growto(0)

def unlocked(stype):
	return unlocks[stype] <= level

def getcost(costtype):
	if costtype == "grow":
		return growcost()
	else:
		return costs[costtype]

def canspend(costtype):
	amount = getcost(costtype)
	return money >= amount

def spend(costtype):
	global money
	amount = getcost(costtype)
	if money < amount:
		return False
	money -= amount
	return True

def earn(amount):
	global money
	money = min(money + amount, maxmoney)

def growcost():
	return growcosts[level]

def growpop():
	return growpops[level]

def growto(newlevel):
	global maxheight, level, maxmoney
	from . import grid, view
	level = newlevel
	maxheight = maxheights[newlevel]
	maxmoney = maxmoneys[newlevel]
	view.setceiling(maxheight)
	for y in range(0, maxheight):
		segs = ((0, y), (0, y + 1)), ((y, y), (y + 1, y + 1))
		for seg in segs:
			grid.addsegment(seg)

def getpop():
	return sum(obj.pop for obj in things)

def cangrow():
	from . import grid
	if level == 0:
		return money < 30
	if level == 1:
		return len(grid.grid.structures) > 0
	if level == 2:
		return getpop() >= 1
	if level == 3:
		return getpop() >= 2
	if level == 4:
		return getpop() >= 5
	if level == 5:
		return getpop() >= 30
	return False

def grow(force = False):
	if not force:
		if not cangrow():
			return False
		if not spend("grow"):
			return False
	growto(level + 1)

def inbounds(pG):
	xG, yG = pG
	return yG <= maxheight


