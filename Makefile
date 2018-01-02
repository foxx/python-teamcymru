.PHONY: test setup

all:

test:
	pytest

setup:
	pip install -e .
