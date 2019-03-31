Snowcrafter
===========

Entry in PyWeek 27  <http://www.pyweek.org/27/>
URL: https://www.pyweek.org/e/unifac27/
Team: Universe Factory 27
Members: Christopher Night (Cosmologicon)
Assets: Music by Kevin MacLeod. Sound from freesound.org.
License: see LICENSE.txt

Requirements
------------

	python 2.7+ or 3.5+
	pygame 1.9+
	numpy

To install the requirements (for Python 2) on Ubuntu:

	sudo apt install python python-pygame python-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

	python3 run_game.py

The game will connect to the gallery server at universefactory.net each time you load it up. It will
also connect to the server if you choose to upload a design.

If you don't want to get content from the server, or you want to play without an internet
connection, see option for offline mode below.

Controls
--------

* Mouse: left click and drag shapes into the design area.
* Tab: toggle easy mode during gameplay
* Esc: quit (overall progress is saved)
* F10: cycle window resolution
* F11: toggle fullscreen
* F12: take screenshot

Command line options
--------------------

* --res=XXX: specify the window height. Defaults to --res=720
* --tiny: same as --res=360
* --small: same as --res=480
* --large: same as --res=1080
* --fullscreen: start in full screen mode
* --lowres: disable some special effects
* --noaudio: disable all audio
* --nomusic: disable music
* --nosfx: disable sound effects
* --offline: run in offline mode (will not connect to universefactory.net server)
* --reset: delete all saved progress
* --easy: start in easy mode
* --unlockall: unlock all content

