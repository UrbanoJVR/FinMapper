.PHONY: clean install test build run

# Limpia archivos generados
clean:
	rm -rf __pycache__ .pytest_cache .coverage *.egg-info dist build

# Instala dependencias en un entorno pipenv
install:
	pipenv install --dev

# Actualiza pipfile.lock si hay nuevas versiones
update:
	pipenv lock --clear

# Ejecuta tests con pytest
test:
	pipenv run pytest

coverage:
	pipenv run pytest --cov --cov-report term-missing

coverage-html:
	pipenv run pytest --cov --cov-report term-missing --cov-report html

# Verifica linting y calidad de código
lint:
	pipenv run flake8 app tests

# Crea paquetes (si tienes setup.py configurado)
build:
	pipenv run python setup.py sdist bdist_wheel

# Ejecuta la aplicación Flask
run:
	pipenv run flask run

# Load local data for develop environment
load-dev-data:
	sqlite3 data.sqlite < dev-data/categories.sql