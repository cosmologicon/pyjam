import os
from . import settings

def isunlocked():
	return os.path.exists(settings.scorename)
def unlock():
	if isunlocked():
		return
	open(settings.scorename, "w").write("0")
def gethiscore():
	if not isunlocked():
		return None
	return int(open(settings.scorename, "r").read().strip())

