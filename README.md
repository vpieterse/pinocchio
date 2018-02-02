# Pinocchio
[![Build Status](https://travis-ci.org/teampinocchio/pinocchio.svg?branch=master)](https://travis-ci.org/teampinocchio/pinocchio)
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

### Docker Images

#### Development
Included in the repository is a simple Docker image bundling the required version of Python and
Django needed to run it locally. There is a separate Dockerfile for production.

Usage:
- From project root, run `docker-compose` with the development config file:
    - `# docker-compose -f docker-compose-development.yml`
- After everything downloaded, execute `bash` in the container to finish first-time setup:
    - `# docker-compose -f docker-compose-development.yml run dev_server bash` 
- Follow the steps from the installation guide if needed. This would include migrating the  
  database and creating a new superuser.
- After initial setup, the Django development server can be started with `docker-compose`
    - `# docker-compose -f docker-compose-development.yml up`
- Django should now be serving Pinocchio on port 8000 as well as listening for code changes.
- **ADVANCED:** *TODO: How to connect PyCharm to Docker container for remote debugging -> wiki page?*