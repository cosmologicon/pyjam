## Setup

	mkdir gallery
	mkdir uploads
	chmod a+x cgi-bin/*.py

## To upload remote server

In this directory, run:

	scp -r . user@server:path

On remote path, run:

	rm gallery/*.json uploads/*.json

## To run the local server

In this directory, run:

	python3 -m http.server

## To manage uploads

Manually copy uploads from "uploads" directory to "gallery" directory, after verifying there are no
errors.


