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

Game modes
----------

Story/Tutorial: six stages to introduce the mechanics. Drag shapes from the icons on the left into
the wedge-shaped area. The view on the right shows the entire pattern. Completing this mode unlocks
the other three game modes.

Gallery: shows designs that players have uploaded. As a precaution, designs that you upload must be
manually approved before they appear in the gallery. I'll be approving them periodically thoughout
the competition, so check back to see yours.

Free play: Create and upload whatever design you want with no objectives.

Bonus stages: nine additional stages. Completing these stages unlocks additional options in Free
Play mode. Complete the three "Shape" stages to unlock additional shapes, the three "Color" stages
to adjust colors of pieces, and the three "Size" stages to adjust sizes of pieces. All stages also
give you a higher limit on the total number of shapes you can use (up to a maximum of 18).

Controls
--------

* Mouse: left click and drag shapes into the design area.
* Tab: toggle Easy mode during gameplay
* Esc: quit (overall progress is saved - progress within a stage is not saved)
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

