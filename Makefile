install:
	poetry install --no-root

dev:
	poetry run uvicorn app.main:app --reload

test:
	poetry run python -m unittest discover -s app

.PHONY: install dev test
