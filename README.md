# pyjam

Code for my Python game jam entries (PyWeek).

* PyWeek 20 (`horizon`): Beyond the Horizon.

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

### After the deadline (packaging)

Rename the directory to reflect the game name.

Update the README and LICENSE files in the game directory to reflect the game name.

	tar czf gamename.tgz gamename/

TODO: avoid temp files
