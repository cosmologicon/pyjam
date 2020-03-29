Miranda the Lepidopterist
=========================

Entry in PyWeek 29  <http://www.pyweek.org/29/>
URL: https://www.pyweek.org/e/unifac29/
Team: Universe Factory 29
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Requirements
------------

	python 3
	pygame (my version is 1.9.6)
	numpy (my version is 1.13.3)
	scipy.ndimage (my scipy is 0.19.1 and my scipy.ndimage is 2.0)

To install the requirements on Ubuntu:

	sudo apt install python3 python3-pygame python3-numpy python3-scipy

scipy is only needed for certain special effects. See the `noglow` option below if you don't want to install it.

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python3 run_game.py

Background
----------

This game is a prequel (set one generation earlier) to my PyWeek 11 entry, Mortimer the Lepidopterist. If you want to see that game, I recommend the HTML5 port I made.

    https://pyweek.org/e/unifac11/
    http://universefactory.net/lep/

Controls
--------

Tap arrow keys or WASD to move. Tap two keys at once to move diagonal.

Some levels contain sparkling butterflies (other than the yellow goal butterflies). These can be moved. Tap space or enter on their space to guide them, and tap again on an empty space to release them.

Backspace will skip a cutscene or forfeit a level. Esc quits the game. Progress is saved after ever level completion. F12 takes a screenshot.

If you feel like messing with the key bindings, see settings.py.

Mechanics
---------

Once in the air, use butterflies to keep moving! Follow the butterflies' arrows and you'll be able to stay aloft.

  * Blue butterflies (O): standard
  * Orange butterflies (2): double movement. You'll move two spaces away.
  * Green butterflies (X): alternators. Each time you move away from a green butterfly, all green butterflies' arrows will change between two states.
  * Purple butterflies (<>): followers. Each time you move, all purple butterflies' arrows will change to match your motion.
  * Yellow butterflies (!!): reach all three of these to complete the stage.

Command line arguments
----------------------

  * `--fullscreen`
  * `--res=###` - set the vertical resolution in pixels. Default is 720.
  * `--tiny` - same as `--res=360`
  * `--small` - same as `--res=540`
  * `--large` - same as `--res=1080`
  * `--forceres` - keep resolution even in fullscreen mode
  * `--nomusic` - disable music
  * `--nosound` - disable sound effects
  * `--reset` - delete saved progress. You can also just delete savegame.pkl.
  * `--textspeed=##` - control how fast dialog text automatically advances (relative to a default of 1)
  * `--fasttext` - same as `--textspeed=2.5`
  * `--colormode` - color accessibility mode. Different color butterflies will have a symbol drawn over them.
  * `--DEBUG` - run in DEBUG mode. While in DEBUG mode, press F1 to unlock all levels, and F2 to beat the current level.

The following options might help if you want to improve performance.

  * `--nobackground` - disable the background wallpaper
  * `--noglow` - disable the white outline around sprites. With this option the game will not import scipy.
  * `--noshadow` - disable the color phasing effect when the character moves.

Tools used
----------

  * Mapgen4 (`https://www.redblobgames.com/maps/mapgen4/`) for the world map
  * jfxr (`https://jfxr.frozenfractal.com/`) for sound effects
  * Gimp
  * Audacity for downsampling the music

