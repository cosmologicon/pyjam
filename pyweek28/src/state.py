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
		stations.append(things.Station("Counterweight", 10000, progress.capacity))
	if progress.missions == 5:
		stations.append(things.Station("LowOrbiton", 700, progress.capacity))
	if progress.missions == 12:
		stations.append(things.Station("Stationary", 7200, progress.capacity))
	if progress.missions == 20:
		stations.append(things.Station("Last Ditch", 3700, progress.capacity))
	if progress.missions == 30:
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
	for pname in ["worker", "sci", "tech"]:
		if reward == pname:
			things.Pop(pname, stationat(0))
			return "New %s reporting for duty at Ground Control" % things.popnames[pname]

portcapacity = [1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8]

missionstacks = {
	"Skyburg": [
		(("worker",), "tech"),
		(("tech",), "capacity"),
		(("worker", "worker"), "sci"),
		(("worker", "worker"), "capacity"),
		(("worker", "tech", "sci"), "sci"),
		(("tech", "sci", "sci"), "capacity"),
	],
	"Counterweight": [
		(("worker", "tech"), "car"),
		(("worker", "tech", "sci"), "car"),
		(("sci", "sci", "tech"), "car"),
	],
	"LowOrbiton": [
		(("worker", "worker", "sci"), "worker"),
		(("sci", "sci", "tech"), "sci"),
		(("worker", "worker", "worker", "tech"), "worker"),
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
		

