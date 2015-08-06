Testing for PyWeek
------------------

This subdirectory is to test pygame functions so that collaborators can check that the game will run
on their system before the competition starts.

Run the test game from the command line:

	python run_game.py

Or if you have pygame for python3 installed:

	python3 run_game.py

Things to check (all should be "yes"):

	1. Does pressing Esc quit the game?
	1. Can you close the window to quit the game (not in fullscreen mode)?
	1. Does fullscreen mode take up most of your screen?
	1. Does the white circle appear roughly circular (not stretched or squashed)?
	1. Is the mouse cursor visible when the mouse moves over the window?
	1. Does the sound play when you click the button without a significant delay?
	1. Does the sound play without being clipped or cut off?
	1. Does the sound play at about the same volume as when you open the sound file directly (in the data directory)?
	1. Do the colors on the Earth image appear roughly correct?
	
	


