all: fmt test build

prepare:
	pipenv install --dev
	npm install

fmt:
	autopep8 -r . --in-place

test:
	flake8 . --exclude node_modules
	cd server && python -m unittest discover
	cd web && npm run lint && CI=true npm run test

build:
	cd web && npm run build
