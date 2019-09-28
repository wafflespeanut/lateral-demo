all: fmt test

fmt:
	autopep8 -r . --in-place

build: fmt

test: build
	flake8 .
	cd server && python -m unittest discover
