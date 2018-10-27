from __future__ import print_function

from . import settings, sound

# play dialog
def trigger(convo):
	sound.manager.current_dialog = convo
	sound.manager.current_dind = 0
	sound.manager.PlayVoice(convo+'1')

def pause():
	sound.manager.PauseVoice()

def get_current_dialog():
	if sound.manager.current_dialog == None:
		return None
	else:
		return (sound.manager.current_dialog, sound.manager.current_dind+1) # (dialog letter A-B-C, number 1,2,3)



