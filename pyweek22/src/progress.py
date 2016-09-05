# Overall game progress, scores, etc.
import os.path
from . import util, settings

try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import settings

completed = set()  # levels completed
heard = set()  # dialogs heard

def complete(level):
	completed.add(level)
	save()

def getprogress():
	return completed, heard

def setprogress(obj):
	global completed, heard
	completed, heard = obj

def save():
	filename = settings.progresspath
	util.mkdir(filename)
	pickle.dump(getprogress(), open(filename, "wb"))

def load():
	filename = settings.progresspath
	if not os.path.exists(filename):
		return
	setprogress(pickle.load(open(filename, "rb")))

