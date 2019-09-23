# Handy module for keeping module-level globals encapsulating the game state.

# TODO: autosave and load on startup.

# Height of the top of the elevator in km.
top = 10000
# Radius of the cable in km.
radius = 1

stations = []

def currentstation():
	from . import view
	for station in stations:
		if abs(station.yG - view.yG0) < 3:
			return station
	return None

def currentstationname():
	s = currentstation()
	return s.name if s is not None else ""

