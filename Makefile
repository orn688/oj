shell = /bin/bash

.PHONY:
	fmt lint test

fmt:
	pipenv run black .
	pipenv run isort --recursive .

lint:
	pipenv run flake8
	pipenv run black --check --diff .
	pipenv run isort --recursive --check-only --diff --recursive .

test:
	pipenv run pytest --verbose --durations=5
