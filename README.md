# Pinocchio
[![Waffle.io - Columns and their card count](https://badge.waffle.io/teampinocchio/pinocchio.svg?columns=all)](https://waffle.io/teampinocchio/pinocchio) 
[![Stories in Ready](https://badge.waffle.io/teampinocchio/pinocchio.png?label=ready&title=Ready)](https://waffle.io/teampinocchio/pinocchio)

Pinocchio is a system which should assist researchers, and group managers to monitor team activities and to allocate teams. In the capstone course of the Department of Computer Science of the University of Pretoria the system is used for regular peer assessments. The system analyses student  reports to determine participatory styles of students. The participatory styles as well as other personal data such as academic standing and personality attributes can be used to allocate teams.  

-------------

### Installation Instructions
- Clone the Pinocchio repository and `cd` into it
    - `git clone https://github.com/teampinocchio/pinocchio.git`
    - `cd pinocchio/`
- _(Recommended)_ Create a new Python 3 virtual environment
    - Create it: `python3 -m venv ./environment`
    - Activate it: `source ./environment/bin/activate`
- Install Django **1.11** and other packages
    - `pip install -r ./requirements.txt`
- Apply Database Migrations
    - `python manage.py migrate`
- Load required data into database
    - `python manage.py loaddata QuestionGroupings`
- Create root user
    - `python manage.py createsuperuser` 
- Run the server
    - `python manage.py runserver`
    
You should now be able to log in with the superuser's userid and password.

-------------


### Deployment Instructions
The default configuration is loaded from `/pinocchio/baseSettings.py` which in turn imports extra
settings from `/pinocchio/globalSettings.py`. The current base settings is set up for deploying locally.

To use your own settings file, append the following line at the end of your custom settings script:
- `from pinocchio.globalSettings import *`

This will pull all extra settings from the `globalSettings.py` script.

We prefer [deploying Pinocchio with WSGI.](https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/)

-------------
