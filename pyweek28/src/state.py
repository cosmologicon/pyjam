# Handy module for keeping module-level globals encapsulating the game state.

# TODO: autosave and load on startup.

# Height of the top of the elevator in km.
top = 10000
# Radius of the cable in km.
radius = 1

stations = []

def stationat(z, dz = 0):
	for station in stations:
		if abs(station.z - z) <= dz:
			return station
	return None

def carat(z, A, dz = 0):
	for car in cars:
		if abs(car.z - z) <= dz and A == car.A:
			return car
	return None

def currentstation():
	from . import view
	return stationat(view.zW0, dz = 3)

def currentstationname():
	s = currentstation()
	return s.name if s is not None else ""

def currentcar():
	from . import view
	return carat(view.zW0, view.A, dz = 3)

class progress:
	capacity = 1
	cars = 2
	carupgrades = 0
	missions = 0
	done = False



def completemission(reward):
	from . import things, view
	progress.missions += 1
	if progress.missions == 2:
		stations.append(things.Station("Upzidazi", 10000, progress.capacity))
	if progress.missions == 6:
		stations.append(things.Station("Lorbiton", 700, progress.capacity))
	if progress.missions == 13:
		stations.append(things.Station("Flotogorb", 7200, progress.capacity))
	if progress.missions == 17:
		stations.append(things.Station("Ettiseek", 3700, progress.capacity))
	if progress.missions == 20:
		progress.done = True
		
	if reward == "capacity":
		progress.capacity += 1
		for station in stations:
			station.capacity = max(progress.capacity, station.capacity)
		return "Station capacity upgraded"
	if reward == "car":
		if len(cars) >= 8:
			progress.carupgrades += 1
			return "Car speed upgraded"
		A = (progress.cars * 3) % 8
		progress.cars += 1
		cars.append(things.Car(0, A))
		return "New car added on %s track" % (view.Anames[A])
	for pname in things.popnames:
		if reward == pname:
			things.Pop(pname, stationat(0))
			if pname == "porter":
				return "New %s reporting for duty at Ground Control. This crew member allows extra ports to be open." % things.popnames[pname]
			if pname == "fixer":
				return "New %s reporting for duty at Ground Control. This crew member automatically fixes cars." % things.popnames[pname]
			return "New %s reporting for duty at Ground Control" % things.popnames[pname]

portcapacity = [1, 2, 3, 4, 5, 6, 7, 8]

missionstacks = {
	"Skyburg": [
		(("worker",), "tech"),
		(("tech",), "capacity"),
		(("worker", "worker"), "sci"),
		(("tech", "sci"), "capacity"),
		(("worker", "worker", "sci"), "sci"),
		(("tech", "sci", "sci"), "porter"),
		(("worker", "worker", "worker"), "capacity"),
		(("worker", "worker", "worker", "sci"), "fixer"),
		(("worker", "sci", "tech", "tech"), "capacity"),
		(("sci", "sci", "sci", "sci", "tech"), "capacity"),
		(("worker", "sci", "tech", "tech", "tech", "tech"), "capacity"),
		(("worker", "worker", "worker", "worker", "worker", "worker", "tech"), "capacity"),
	],
	"Upzidazi": [
		(("worker", "tech"), "car"),
		(("worker", "tech", "sci"), "car"),
		(("sci", "sci", "tech"), "car"),
		(("worker", "worker", "sci", "tech"), "car"),
		(("sci", "sci", "sci", "tech"), "car"),
		(("worker", "tech", "tech", "tech"), "car"),
		(("worker", "sci", "sci", "sci", "sci"), "car"),
		(("worker", "worker", "worker", "worker", "worker", "sci"), "car"),
	],
	"Lorbiton": [
		(("tech"), "worker"),
		(("worker", "worker", "sci"), "tech"),
		(("sci", "sci", "tech"), "sci"),
		(("worker", "worker", "worker", "tech"), "tech"),
		(("worker", "worker", "sci", "sci", "sci"), "sci"),
		(("sci", "sci", "tech", "tech", "tech"), "porter"),
		(("worker", "worker", "worker", "worker", "worker", "sci"), "tech"),
	],
	"Flotogorb": [
		(("worker", "worker", "sci"), "worker"),
		(("sci", "sci", "tech"), "sci"),
		(("worker", "worker", "worker", "tech"), "worker"),
		(("sci", "sci", "sci", "tech", "tech"), "tech"),
		(("worker", "worker", "worker", "worker", "worker", "sci"), "worker"),
	],
	"Ettiseek": [
		(("worker", "worker", "sci", "tech"), "fixer"),
		(("sci", "sci", "tech", "tech", "tech"), "tech"),
		(("worker", "worker", "worker", "worker", "worker", "sci"), "porter"),
	],
}


def updatemissions():
	from . import quest
	for station in stations:
		if station.mission is None and station.name in missionstacks:
			stack = missionstacks[station.name]
			if stack:
				need, reward = stack.pop(0)
				station.setmission(need, reward)
		

