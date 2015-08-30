Beyond the Horizon
==================

Entry in PyWeek 20  <http://www.pyweek.org/20/>

Universe Factory 20 <https://www.pyweek.org/e/unifac20/>

Team Members:
Christopher Night (Cosmologicon)
Mary Bichner (marybee)
Charles McPillan
Leo Stein
Molly Zenobia
Randy Parcel

License: see below

Requirements
------------

Requires Python and Pygame (with surfarray support). Pygame requires numpy, SDL_image, and
SDL_mixer.

Tested on Ubuntu Linux with Python 2.7.6 + Pygame 1.9.1release, and Python 3.4.0 + Pygame 1.9.2a0.

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame python-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

	python run_game.py

Default resolution is 854x480 in windowed mode. Resolution command-line options are:

	--fullscreen : run in fullscreen mode (can also press F11 in-game)
	--1080 : run at 1920x1080 in windowed mode
	--720 : run at 1280x720 in windowed mode

Any other 16x9 resolution can be set in src/settings.py.

Playing the Game
----------------

Follow the in-game instructions. Full controls are:

	arrows or WASD: move
	space or shift or enter or Z: teleport
	backspace: emergency transport
	esc: quit
	F5: save game (also auto-saves when you quit)
	F11: togggle fullscreen
	F12: screenshot

See src/settings.py for more custom options, including setting custom key bindings.

Please visit the entry page if you have any difficulties with the game.

Source Code License
-------------------

Source code is by Christopher Night, released CC0.

Asset License
-------------

You have permission to redistribute all assets along with this game.

Fonts from Google Web Fonts. See the data/fonts directory for individual font licenses.

Spaceship sprite from http://opengameart.org/content/basic-airship CC-BY, by Alex Pineda.

Music copyright Mary Bichner.

Avatar images copyright Molly Zenobia.

All other assets are CC-BY, Team Universe Factory.
