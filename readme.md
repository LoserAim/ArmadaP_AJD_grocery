# How to run this web server
Shown below are a series of steps to take to run this application.

1. Setup a virtual environment and activate virtual environment
2. install the `requirements.txt` file using `pip`
3. Set the flask app to target `app.py`. Examples shown below:
Bash
```bash
export FLASK_APP=app
```
Command Prompt
```cmd
set FLASK_APP=app
```
4. Run this python command to start web server: `python -m flask run`

# How to run tests
All tests can be ran using pytest. If installed correctly, a user can run pytest from the command line in the directory. Like so: `python -m pytest`
