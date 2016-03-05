Shattered World
===============

Entry in PyWeek 21  <http://www.pyweek.org/21/>
URL: https://www.pyweek.org/e/unifac21/
Team: Universe Factory 21
Members: Christopher Night (Cosmologicon), Mary Bichner (marybee), John Pilman (typhonic), Charles McPillan, Molly Zenobia, Randy Parcel, Monica Vargas
License: see LICENSE.txt

Requirements
------------

	python 2.7+ or 3.3+
	pygame 1.9+

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame python-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

Controls
--------

* Left click on ship to select
* Left drag to select multiple ships
* Shift+click or ctrl+click to select multiple ships
* Tab to cycle between ships

* Right click or Enter to send ships to cursor

* Arrow keys or WASD to move the camera
* Middle drag to move the camera
* Space to pan the camera to the current ship
* Hold space to follow current ship

* M to bring up the map

* Esc to quit

Command-line arguments
----------------------

    --restart : delete saved game and start over
    --small : 640x360 resolution (default is 854x480)
    --large : 1280x720 resoultion
    --huge : 1920x1080 resolution
    --lowres : don't draw a couple special effects
    --fullscreen : start in fullscreen mode

Please see settings.py for accessibility options. The keys may be specified with the `keys`
variable, and the in-game colors may be specified with the `ncolors` variable.
