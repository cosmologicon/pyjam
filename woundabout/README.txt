Woundabout
==========

Entry in PyWeek 32  <http://www.pyweek.org/32/>
URL: https://www.pyweek.org/e/unifac32/
Team: Universe Factory 32
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Requirements
------------

Developed using:

	Python 3.8.10
	Pygame 1.9.6


To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python3 run_game.py

See below for command-line options

Controls
--------

Keyboard.

* Arrows or WASD: move
* Space or Enter: bite/release
* Esc: bring up help screen, exit to main menu, quit
* F1: toggle controls, between absolute and relative
* F2: toggle camera, between fixed and follow
* F3: toggle auto-bite
* F4: adjust sfx volume
* F5: adjust music volume
* F10: adjust resolution
* F11: toggle fullscreen
* F12: take screenshot",

How to play
-----------

There are in-game instructions in Adventure mode, so I recommend checking that out first.

Similar to the classic game Snake, but instead of running an object to collect or activate it, you
must encircle (go around) it and bite your tail. Objects are shown in the help screen in-game (press
Esc):

* Energy: increase snake length
* Regular key (blue): unlock the next area. In Endless mode, activate all keys to continue to the
next stage.
* Rotating key: this key is rotating either clockwise (yellow) or counter-clockwise (pink). You must
encircle the key in the corresponding direction in order to activate it.
* Numbered key: can only be activated by simultaneously encircling the given number of keys.
* Disruptor (red): disrupts activation. Disruptors may not be activated. Furthermore, if you are
encircling any disruptor, then you will not be able to activate any energy or keys you are
encircling.

Strategy tips
-------------

Your head must be in about the same place as your tail to be able to bite, and also facing in
about the same direction. Your mouth will open when you have an opportunity to bite. You can turn
on auto-bite with F3.

For rotating (yellow and pink) keys, the color of the key should match the side of the snake that's
on the inside.

Toggle the control scheme with F1. For best results, try them both out for a few minutes. Absolute
is more like classic Snake and is a bit more intuitive. Relative turns you left or right based on
the way the snake is facing. Relative is recommended for advanced play.

In relative control mode, hold up to make wider turns, and hold down to make sharper turns.

Endless mode gets difficult fast after a few stages. By Stage 12 it's really hard. There are 20
different layouts in total. After Stage 20 it repeats, but faster.

For advanced play in Endless mode, you should learn the pattern of when disruptors appear. At first,
every energy collected will leave a disruptor. After some point (depending on your starting length),
only every 3rd energy will leave a disruptor. Collect them in the order that puts the disruptors
out of your way. If you collect more than one at once, the game assigns them some order, so you may
need to get one at a time to be safe.

Command-line options
--------------------

* `--reset`: delete saved game
* `--fullscreen: fullscreen mode
* `--res=###: change resolution
* `--nosfx`: sound volume to 0
* `--nomusic`: music volume to 0
* `--nosound`: both to 0

To reset all options, delete the file settings.pkl.

