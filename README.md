# Hiring

Installation Instructions
If you want to work with this project or create a version of it make sure to follow the steps below!

Make sure to install Python 3, pip and virtualenv

Create a project folder

    $ mkdir project
    $ cd project
Create a python 3 virtualenv, and activate the environment to install requirements.

    $ python3 -m venv env
    $ source env/bin/activate
Install the project dependencies from requirements.txt

    (env)$ pip install -r requirements.txt
Clone the repository

    (env)$ git clone https://github.com/krishnaa192/Hiring.git
    (env)$ cd django Hiring
You have now successfully set up the project on your environment.

How to run the project?
Make sure you are in env and then do the following each at a time.

(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py createsuperuser
(env)$ python manage.py runserver

