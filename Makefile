.PHONY: test all

all:

build:
	docker-compose build app

test: build
	docker-compose run app pytest

shell: build
	docker-compose run app

setup:
	pip install -e .

clean:
	docker-compose down -v
	find . -type d -iname '__pycache__' -exec rm -rf '{}' \;
	find . -type d -iname '.cache' -exec rm -rf '{}' \;
