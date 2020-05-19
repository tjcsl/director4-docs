---
Title: Django
...

# Django

Note: This page is not intended as a "Getting started with Django" tutorial. It covers how to deploy an *existing* Django application on Director.

**WARNING: NEVER use `./manage.py runserver` to deploy your application on Director. This has massive security issues and is very CPU-intensive compared to proper deployment methods. The Sysadmins reserve the right to disable and/or remove without warning any site that is using `./manage.py runserver`.**

First, select a Python Docker image for your site (see [Custom Docker Images](/quick-start/site-configuration.md#custom-docker-images)). Then, in the terminal, create a virtual environment with `virtualenv public/venv`. Activate the virtual environment with `source public/venv/bin/activate`, then install any Python packages you need (like Django) with `pip install <package names>`. If you later need to modify something in your virtual environment, you can always re-activate it with `source public/venv/bin/activate`.

You can use the `run.sh` template that comes with the Python Docker images, but you will need to comment out the command labeled "Flask," uncomment the command labeled "Django," and replace `<name>` with the name of your application.

To serve static files, we recommend using [`whitenoise`](http://whitenoise.evans.io/en/stable/). Setup is simple: just `pip install whitenoise` and then follow WhiteNoise's [Django Quick Start](http://whitenoise.evans.io/en/stable/#quickstart-for-django-apps).

### Database access

After [setting up a database](/databases/quick-start.md), see either the [PostgreSQL Django setup instructions](/databases/postgresql.md#django) or the [MySQL Django setup instructions](/databases/mysql.md#django), as appropriate.
