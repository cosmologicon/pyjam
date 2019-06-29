# pyjam

Code for my Python game jam entries (PyWeek).

* PyWeek 20 (`horizon`): Beyond the Horizon.
* PyWeek 21 (`shattered`): Shattered World.
* PyWeek 22 (`zome`): Dr. Zome's Laboratory.
* PyWeek 23 (`final-choice`): The Final Choice.
* PyWeek 24 (`faraway`): Faraway Near.
* PyWeek 25 (`otherworlder`): Otherworlder.
* PyWeek 26 (`odyssey`): Storm Drain Odyssey.

## Setup process

Notes for myself.

### When PyWeek is announced

Begin by creating the directory:

	git clean -f -X skellington
	cp -r skellington pyweek##
	git add pyweek##

Update `pyweek##/README.txt` to change references (`##`) to the appropriate number.

Make initial git checkin.

### Development during PyWeek

Place modules in the `src` subdirectory. Within modules, use relative imports to import other
modules:

	from . import module1, module2

Modules may be executed as standalone scripts from the command line:

	python -m src.module1

### End of development

Check the list of pygame tips to make sure you didn't make any cross-platform mistakes:

	https://github.com/cosmologicon/pyjam/wiki/pygame-notes-and-tricks

### After the deadline (packaging)

Rename the directory to reflect the game name.

Make sure DEBUG mode is off by default in the checkin.

Make sure music and data is pointing to the correct place.

Update the README and LICENSE files in the game directory to reflect the game name.

	tar czf gamename.tgz gamename/

TODO: avoid temp files
