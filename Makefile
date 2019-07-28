shell = /bin/bash

.PHONY:
	fmt lint test

fmt:
	pipenv run black .
	pipenv run isort --recursive .

lint:
	pipenv run mypy --ignore-missing-imports .
	pipenv run black --check --diff .
	pipenv run isort --recursive --check-only --diff --recursive .
	pipenv run flake8

test:
	pipenv run pytest --durations=5
