THE TIDE SUMMONER
=================

Entry in PyWeek 30  <http://www.pyweek.org/30/>
URL: https://www.pyweek.org/e/unifac30/
Team: Universe Factory 30
Members: Christopher Night (Cosmologicon), Mary Bichner (marybee)
License: see LICENSE.txt

Requirements
------------

	python 3.5+
	pyopengl
	pygame 1.9+

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python3 run_game.py

Controls
--------

  * Arrow keys or WASD: move
  * Space or Enter: tow/release the Tide Summoner (after it appears)
  * Tab: toggle zoom (not available at the start of the game)
  * Esc: quit
  * F10: change resolution
  * F11: toggle fullscreen
  * Hold Ctrl: hint (show current objective)
  * F1: cheat (skip current objective)

Hints and cheats
----------------

The game is intended to be solvable without using any hints, but feel free to use them if you get
stuck, especially if you suspect there's a bug!

Hold down the Ctrl key to view the current objective. Alternately, start the game with the
`--easymode` flag to have the objective always visible.

Press F1 to complete the current objective and skip ahead.

Color swapping
--------------

Some puzzles require you to distinguish certain colors: red, yellow, blue, white, and black. If you
wish to tweak the colors used, you edit the variable `colors` in `src/settings.py`.

Command line flags
------------------

  * `--res=###`: set vertical resolution. e.g. `--res=480` is 480p
  * `--fullscreen`: start in fullscreen mode
  * `--easymode`: make hints always visible
  * `--reset`: delete saved game and start over. By default the game is auto-saved every 5 seconds.
