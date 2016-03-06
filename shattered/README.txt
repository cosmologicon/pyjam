Shattered World
===============

Entry in PyWeek 21  <http://www.pyweek.org/21/>
URL: https://www.pyweek.org/e/unifac21/
Team: Universe Factory 21
Members: Christopher Night (Cosmologicon), Mary Bichner (marybee), John Pilman (typhonic), Charles McPillan, Molly Zenobia, Randy Parcel, Monica Vargas
License: see `LICENSE.txt`

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

Camera:

* Arrow keys or WASD to move camera
* Middle-button drag to move camera
* Space to center on current ship
* Hold space to follow current ship

Selecting ships:

* Left click on a ship or the icon in the upper left to select it
* Double click on any ship or icon to select all ships
* Left-button drag to select multiple ships
* Tab to cycle through ships

Movement:

* Right click to send selected ship to a point
* Enter key emulates right click

Other:

* Click on the minimap (or press M) to view the map
* Press F or F11 to toggle fullscreen
* Press Esc to exit
* Press F12 to take a screenshot (saved in screenshots directory)

Edit the `key` variable in `src/settings.py` to change key bindings.

Edit the `ncolors` variable in `src/settings.py` to change colors used in the game.

Command-line arguments
----------------------

    --restart : delete saved game and start over
    --small : 640x360 resolution (default is 854x480)
    --large : 1280x720 resoultion
    --huge : 1920x1080 resolution
    --lowres : don't draw a couple special effects
    --fullscreen : start in fullscreen mode
    --cheat : start with extra upgradons
