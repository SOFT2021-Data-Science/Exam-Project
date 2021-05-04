This will be hosted with gunicorn.
Gunicorn can't be used with windows.

##
For development purposes, the backend can be run with:
> python main.py

## Poetry guide

cd to back/diagram_webservice
### To enter environment:
>poetry shell

### add packages:
>poetry add insert_your_package_here

### remove packages:
>poetry remove insert_your_package_here

### Whenever you've added or removed packages: 
>poetry export -f requirements.txt --output requirements.txt 

This requirements.txt is a recipe for the required modules. It's so the server'scontainer installs the correct packages. It's also required for people who use venv can use our project

### Whenever someone else has made changes and you need to update your shell: 
>poetry update

### Run tests with:
>nose2 -v