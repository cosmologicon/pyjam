BurgleCast
==========

Entry in PyWeek 35  <http://www.pyweek.org/35/>
URL: https://www.pyweek.org/e/unifac35/
Team: Universe Factory 35
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Game Info
---------

Turn-based puzzle game on a hex grid. Play as a jewel thief live streaming his exploits. Stay in
the shadows of the security system to avoid being caught.

There are 4 quick tutorial stages, 7 regular stages, and 1 very optional final free-play stage.
I recommend completing at least the tutorial plus one more stage (either London or Copenhagen)
before rating the game. This should take 5-10 minutes at most. The entire game might take 30
minutes, but it depends a lot on how tricky you find the puzzles. Progress is saved when you
complete a stage.

How it fits the theme (In the Shadows): the main mechanic is blocking beams of light to remain
out of sight.

Requirements
------------

Python 3 and Pygame. Developed using Python 3.10.6 and Pygame 2.1.2.

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python3 run_game.py

Controls
--------

Use the mouse. Click and drag on the character or on a sculpture to move it. Also:

* Backspace: undo
* R: restart
* Escape: quit
* F1: cheat (add +1 turn to current stage)
* F10: change resolution
* F11: toggle fullscreen
* F12: screenshot

Command line options
--------------------

Note: these were added after the coding deadline. Feel free to ignore them.

* `--reset`: Reset saved progress.
* `--unlockall` (cheat): Unlock all stages.
* `--fullscreen`: Start in fullscreen mode.
* `--res=###`: Set starting vertical resolution, e.g. `--res=1080`.


