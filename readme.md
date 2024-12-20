# Developers guide

## Python pipenv management

````
#if you don't have pipenv installed
brew install pipx
pipx ensurepath
pipx install pipenv

#check if you have created venv
pipenv --venv

#create it
pipenv install

#update lock (when change pipfile)
pipenv lock
````


## Database management

To create and update local sqlite database:

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
´`´++

## Language and translations

Add new messages into the specific file.

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

