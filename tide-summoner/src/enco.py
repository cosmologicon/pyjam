# entity/component tool for small games, by Christopher Night
# https://github.com/cosmologicon/enco

# Usage: subclass enco.Component to create a component. Use an instance of the component as a
# decorator on an entity class.
class Component(object):
	def __call__(self, cls):
		def componentmethod(methodname):
			def func(*args, **kwargs):
				ret = None
				for method in cls._componentmethods[methodname]:
					ret = method(*args, **kwargs)
				return ret
			return func
		componentflag = "_" + cls.__name__ + "_componentified"
		if not hasattr(cls, componentflag):
			setattr(cls, componentflag, True)
			methods = {}
			for attrname in dir(cls):
				if attrname.startswith("__"):
					continue
				attr = getattr(cls, attrname)
				if not callable(attr):
					continue
				setattr(cls, attrname, componentmethod(attrname))
				methods[attrname] = [attr]
			cls._componentmethods = methods
		for attrname in dir(self):
			if attrname.startswith("__"):
				continue
			attr = getattr(self, attrname)
			if callable(attr):
				if attrname not in cls._componentmethods:
					cls._componentmethods[attrname] = []
					setattr(cls, attrname, componentmethod(attrname))
				cls._componentmethods[attrname].insert(0, attr.__func__)
			elif not hasattr(cls, attrname):
				setattr(cls, attrname, attr)
		return cls

