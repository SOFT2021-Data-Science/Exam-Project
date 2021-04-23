This will be hosted with gunicorn.
Gunicorn can't be used with windows.
For development purposes, the backend can be run with:
> python main.py

<h4>Poetry guide:</h4>
<ul>
    <li>cd to back/diagram_webservice</li>
    <li>To enter environment:<br>
    > poetry shell
    </li>
    <li>add packages: <br>> poetry add insert_your_package_here</li>
    <li>remove packages: <br>> poetry remove insert_your_package_here</li>
    <li>Whenever you've added or removed packages: 
    <br>> poetry export -f requirements.txt --output requirements.txt 
    <br>This requirements.txt is a recipe for the required modules. It's so the server's container installs the correct packages. It's also required for people who use venv can use our project
    </li>
    <li>Whenever someone else has made changes and you need to update your shell: <br>>  poetry update</li>
</ul>
    


<p>Run tests with nose2 -v</p>