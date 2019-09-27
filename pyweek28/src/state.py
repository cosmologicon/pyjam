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

