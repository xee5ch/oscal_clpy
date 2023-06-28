clean:
	rm -rf dist

install:
	python -m poetry install

test:
	python -m poetry run pytest
