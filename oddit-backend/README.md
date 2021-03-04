# oddit-backend
Backend for Oddit software

# Collaboration rules
As users of the free version of GitHub Organization, I cannot set protection on branches. Nonetheless, do NOT push to master directly.

# Starting the project
After cloning the project on GitHub, run `pipenv install` to install all the required dependencies.

Pipenv is a virtual environment used in Python to manage dependencies.

Next:
- `pipenv shell`: Always enter the virtual environment to get the correct python version anf the correct dependencies versions. 
- `cd backend`
- `python manage.py runserver`
- Open your browser to `http://127.0.0.1:8000/` and check that it is running.
