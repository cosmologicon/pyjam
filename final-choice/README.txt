The Final Choice
================

Entry in PyWeek 23  <http://www.pyweek.org/23/>
URL: https://www.pyweek.org/e/unifac23/
Team: Universe Factory 23
Members: Christopher Night (Cosmologicon), Charles McPillan (EnigmaticArcher), Mary Bichner (marybee), Magnus Drebenstedt (Goldhand) and others
License: see LICENSE.txt

Requirements
------------

	python 2.7+ or 3.5+
	pygame 1.9+

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame python-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

Command-line options are as follows:

    --fullscreen : start up in fullscreen mode (F11 to toggle in-game)
    --portrait : start up in vertical (portrait or arcade) mode (F10 to toggle in-game)
    --miracle : start up in Miracle Mode (see below)
    --res=XXX : set the vertical resolution. Aspect ratio is 16:9. Default is 480p.
        (In vertical mode, this option sets the horizontal resolution, and the aspect ratio is 9:16.)
    --big : same as --res=720
    --huge : same as --res=1080
    --lowres : disable some graphical effects
    --restart : delete saved games and start from the beginning
    --nomusic : disable music
    --nosound : disable all sound, including music


Controls
--------

    Move: Arrow keys or WASD (works on Dvorak too)
    Shoot: space or enter or shift or control or Z
    Togggle auto-shoot mode: Tab or Caps Lock
    Toggle vertical (portrait) mode: F10
    Toggle fullscreen mode: F11
    Screenshot: F12
    Quit: Escape

Ending
------

There are three endings depending on the choices you make in the game: Bad, Good, and Best.

The good and best endings require you to save all members of the Hawking crew in a single
playthrough.

Miracle Mode
------------

This is the easy mode of the game, which you can run with the "--miracle" command line option. In
miracle mode, you have more shield and it regenerates faster. Also, any crew members you have
rescued on previous playthroughs will start the game out as already rescued, and you will not have
to sacrifice anything to save them. Therefore miracle mode lets you use several playthroughs,
rescuing some of the crew each time, to achieve the good and best endings.

