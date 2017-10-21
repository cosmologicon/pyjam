Faraway Near
============

Entry in PyWeek 24  <http://www.pyweek.org/24/>
URL: https://www.pyweek.org/e/unifac24/
Team: Universe Factory 24
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Requirements
------------

	python 2.7+ or 3.3+
	pygame 1.9+
	numpy

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame python-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

How to Play
-----------

Keyboard controls are explained in game. Use the arrow keys or WASD (also works in Dvorak) to move
forward and back, and space, enter, or up to jump. Esc to quit.

Progress is saved automatically.

About the Game
--------------

Faraway Near is an infinite runner platformer action game. There is a story mode, which also acts as
a tutorial. After completing the story mode, the endless mode is unlocked. There's a couple new
things in endless mode, but mostly it's stuff you've already seen. If you progress far enough, the
landscape changes colors around you and the action speeds up.

If you restart endless mode, you will get a head start equal to 1/2 your current high score.

If you get to 160 meters in endless mode, you've seen everything there is in the game. I suggest you
at least finish the story mode to get a feel for the game before rating the game. If you find story
mode too hard, see the --speed option below.

Command Line Options
--------------------

	--speed=###: adjust game speed (for story mode only), e.g. --speed=0.5 plays at 1/2 speed
	--slow: same as --speed=0.75
	--unlock: unlock endless mode
	--reset: delete story mode progress
    --fullscreen: start in fullscreen mode (can also press F11 in game)
    --res=###: specify vertical resolution, e.g. --res=640 (default is 480)
    --lowfi: remove some special effects (for slower systems)
    --nomusic: disable music
    --nosfx: disable sound effects
    --noaudio: disable music and sound effects
