# Developers guide

## Update requirements

pip freeze > requirements.txt

## Language and translations

Add new messages into the specific file.

Please make sure you are respecting the alphabetical order to sort the translation dictionaries keys.

Compile the translation files:

````
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
pybabel init -i messages.pot -d translations -l es
pybabel init -i messages.pot -d translations -l en
pybabel compile -d translations -l es
pybabel compile -d translations -l en
````

