import random, math
import dialog, state, gamescene, buildscene, scene, starmap, bosses, vista, settings, sound

class Quest(object):
	def think(self, dt):
		pass
	def complete(self):
		state.state.quests.remove(self)
	def home(self):
		return scene.top() is buildscene
	def addquest(self, quest):
		state.state.quests.append(quest)
	def addinterest(self, iname, pos = None):
		state.state.interests.add(iname)
		if pos is not None:
			obj = getattr(state.state, iname)
			obj.x, obj.y = pos
	def removeinterest(self, iname):
		state.state.interests.remove(iname)
	def unlock(self, modulename):
		if modulename not in state.state.unlocked:
			state.state.unlocked.append(modulename)

# Tutorial dialogs
class IntroQuest(Quest):
	def __init__(self):
		dialog.play("cometomother")
		self.addinterest("mother")

	def think(self, dt):
		if self.home():
			dialog.playfirst("hookupmodule")
		if not self.home() and "drill" in state.state.hookup:
			dialog.playfirst("howtodrill")
		if self.home() and state.state.bank >= settings.modulecosts["laser"]:
			dialog.playfirst("buylaser")
		if not self.home() and "laser" in state.state.hookup and state.state.bank >= 10:
			self.addquest(Baron1Quest())
			self.complete()

# Set up first encounter with the baron and first boss battle
class Baron1Quest(Quest):
	amount = 50

	def __init__(self):
		dialog.playfirst("cometobaron1")
		self.addinterest("baron", pos = starmap.ps["baron1"])
		state.state.ships.append(state.state.baron)
		self.lasttalk = 0
		
	def think(self, dt):
		if self.lasttalk:
			self.lasttalk = max(self.lasttalk - dt, 0)
		else:
			dx, dy = state.state.you.x - state.state.baron.x, state.state.you.y - state.state.baron.y
			if dx ** 2 + dy ** 2 < 2 ** 2:
				self.lasttalk = 10
				if state.state.bank < self.amount:
					dialog.play("wheresmymoney")
				else:
					state.state.bank -= self.amount
					sound.play("buy")
					state.state.baron.fadeable = True
					dialog.play("findthesupply")
					self.addquest(Boss1Quest())
					self.removeinterest("baron")
					self.complete()

class Boss1Quest(Quest):
	def __init__(self):
		self.addinterest("supply", pos = starmap.ps["supply"])
		state.state.ships.append(state.state.supply)
		self.boss = bosses.Boss1(starmap.ps["supply"])
		state.state.boss = self.boss
		state.state.ships.append(self.boss)

	def think(self, dt):
		self.complete()

class Act2Quest(Quest):
	def think(self, dt):
		if not self.home() and "turbo" in state.state.hookup and state.state.bank >= 50:
			self.addquest(Baron2Quest())
			self.complete()

class Baron2Quest(Quest):
	amount = 200

	def __init__(self):
		dialog.playfirst("cometobaron2")
		self.addinterest("baron", pos = starmap.ps["baron3"])
		state.state.ships.append(state.state.baron)
		self.lasttalk = 0
		
	def think(self, dt):
		if self.lasttalk:
			self.lasttalk = max(self.lasttalk - dt, 0)
		else:
			dx, dy = state.state.you.x - state.state.baron.x, state.state.you.y - state.state.baron.y
			if dx ** 2 + dy ** 2 < 2 ** 2:
				self.lasttalk = 10
				if state.state.bank < self.amount:
					dialog.play("wheresmymoney2")
				else:
					state.state.bank -= self.amount
					sound.play("buy")
					state.state.baron.fadeable = True
					dialog.play("findboss2")
					self.addquest(Boss2Quest())
					self.removeinterest("baron")
					self.complete()

class Boss2Quest(Quest):
	def __init__(self):
		self.addinterest("supply", pos = starmap.ps["boss2"])
		state.state.ships.append(state.state.supply)
		self.boss = bosses.Boss2(starmap.ps["boss2"])
		state.state.boss = self.boss
		state.state.ships.append(self.boss)

	def think(self, dt):
		self.complete()

class Act3Quest(Quest):
	def __init__(self):
		self.addquest(EndQuest())
	def think(self, dt):
		import things
		if sum(t.surveyed and isinstance(t, things.Sun) for t in state.state.things) > 2:
			self.addquest(Baron3Quest())
			self.complete()

class Baron3Quest(Quest):
	def __init__(self):
		dialog.playfirst("cometobaron4")
		self.addinterest("baron", pos = starmap.ps["baron4"])
		state.state.ships.append(state.state.baron)
		self.lasttalk = 0
		
	def think(self, dt):
		if self.lasttalk:
			self.lasttalk = max(self.lasttalk - dt, 0)
		else:
			dx, dy = state.state.you.x - state.state.baron.x, state.state.you.y - state.state.baron.y
			if dx ** 2 + dy ** 2 < 2 ** 2:
				state.state.baron.fadeable = True
				dialog.play("findangel10")
				self.removeinterest("baron")
				self.complete()

class EndQuest(Quest):
	def think(self, dt):
		if state.state.angel5.surveyed:
			print "You beat the game. See the README for the cutscene that didn't make it in. Thanks for playing!"
			exit()


