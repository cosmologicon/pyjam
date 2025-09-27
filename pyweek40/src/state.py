
costs = {
	"segment": 1,
	"office": 10,
	"spire": 20,
	"residence1": 1,
	"vending1": 1,
}

level = 0
maxheight = 0
maxheights = [6, 9, 12, 15, 18]
growcosts = [10, 20, 50, 100, 200]
money = 100
maxmoney = 10000
things = []


def init():
	growto(0)

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

def growto(newlevel):
	global maxheight, level
	from . import grid, view
	level = newlevel
	maxheight = maxheights[newlevel]
	view.setceiling(maxheight)
	for y in range(0, maxheight):
		segs = ((0, y), (0, y + 1)), ((y, y), (y + 1, y + 1))
		for seg in segs:
			grid.addsegment(seg)

def grow():
	if not spend("grow"):
		return False
	growto(level + 1)

def inbounds(pG):
	xG, yG = pG
	return yG <= maxheight


