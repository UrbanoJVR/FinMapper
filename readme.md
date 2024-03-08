# Developers guide

## Update requirements

pip freeze > requirements.txt

## Language and translations

Add new messages into the specific file.

Please make sure you are respecting the alphabetical order to sort the translation dictionaries keys.

Commands to generate and compile translation files. Be careful: init command will re-write whole translate
.po files and will not use alphabetical order

````
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d translations
pybabel compile -d translations
````

