# Hack taken from SO. Convert postions and sizes to different resolutions than the default
# http://stackoverflow.com/questions/1060796/callable-modules

# NB: DOESNT WORK

from __future__ import division
import sys

class F(object):
	def __call__(self, *args):
		import settings
		if len(args) == 1:
			return int(round(args[0] * settings.sy / 480))
		else:
			return [int(round(arg * settings.sy / 480)) for arg in args]

sys.modules[__name__] = F()

