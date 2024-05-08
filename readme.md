# Developers guide

## Database management

To create local sqlite database:

````
flask db upgrade
````

Generate script for new migrations:

````
flask db migrate
````

If you want to create empty migration file to insert manual changes:

````
flask db revision
````

## Config pycharm

![Pycharm run configuration](doc_img/flask_run_config_pycharm.png?raw=true "Pycharm run config")

## Update requirements

````
pip freeze > requirements.txt
````

## Language and translations

Add new messages into the specific file.

Please make sure you are respecting the alphabetical order to sort the translation dictionaries keys.

Commands to generate and compile translation files. Be careful: init command will re-write whole translate
.po files and will not use alphabetical order

````
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d app/translations
[edit messages.po files]
[add messages into manual_messages files if not detected by commands]
[copy manual_messages.po content inside messages.po files]
pybabel compile -d app/translations
````

