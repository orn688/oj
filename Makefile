shell = /bin/bash

.PHONY:
	fmt lint test

fmt:
	pipenv run black .
	pipenv run isort --recursive .

lint:
	pipenv run black --check --diff .
	pipenv run isort --recursive --check-only --diff --recursive .
	pipenv run flake8
	pipenv run mypy --ignore-missing-imports .

test:
	pipenv run pytest --verbose --durations=5
