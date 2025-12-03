
# Flask Todo App with GitHub OAuth

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![Render](https://img.shields.io/badge/Deploy-Render-purple)

## Features

- Flask + SQLAlchemy ORM
- GitHub OAuth via Flask-Dance
- SQLite (easy to switch to PostgreSQL)
- Ready for Render deployment
- GitHub Actions CI/CD

### Flask

### SQLAlchemy & SQLite

### Flask-Dance & OAuth

### Render

### Github Actions

## Setup

```bash
git clone <repo-url>
cd flask-todo-oauth
pip install -r requirements.txt
cp .env.example .env
```

## Run

```python -m flask run```

## Explain .env

Set up a APP_SECRET_KEY

## GitHub auth setup for local dev

Register your app on GitHub Developer Settings:

- Go to [GitHub OAuth Apps](https://github.com/settings/developers) [Full Docs](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)
- Create a new OAuth App. ( You will need one for your local development of any FlaskDance sites so I'd build one for that)
- Set "Application name": FlaskDanceLocalDev
- Set "Homepage URL": [http://localhost:5000](http://localhost:5000)
- Set "Application description": For Local FlaskDanceDevelopment
- Set "Authorization callback URL": [http://localhost:5000/login/github/authorized](http://localhost:5000/login/github/authorized) (for local dev).

Get Client ID and create a Client Secret now, copying them into .env

You will also need to set ```OAUTHLIB_INSECURE_TRANSPORT=1``` in .env but only ever do this locally

## Other Auth

[https://flask-dance.readthedocs.io/en/latest/providers.html#providers](https://flask-dance.readthedocs.io/en/latest/providers.html#providers)
[https://flask-dance.readthedocs.io/en/v1.2.0/quickstarts/google.html](https://flask-dance.readthedocs.io/en/v1.2.0/quickstarts/google.html)
[https://flask-dance.readthedocs.io/en/latest/quickstart.html](https://flask-dance.readthedocs.io/en/latest/quickstart.html)
[https://flask-security.readthedocs.io/en/stable/](https://flask-security.readthedocs.io/en/stable/)

## The Database

This code uses [SQLAlchemy](https://www.sqlalchemy.org/) to set up classes that have methods to talk to many [databases](https://docs.sqlalchemy.org/en/20/dialects/index.html) we use SQLite for simplicity here.

### SQLite Viewer extension

The database file is in /instance/

The database can be changed to

## First deployment

Once you have your code how you want

## Deployment on Render

- Add `render.yaml` to repo
- Push to GitHub
- Create Blueprint on Render
- Add environment variables in Render dashboard

## Things we are ignoring

- Persistent records in a database. The current database will be destroyed each time you push to render,  ( we are only testing, not building a real system that works for years).
- Changing database structure SQLAlchemy Migrations. Currently we aren't handling changes to the database structure so you need to delete the local .db and start again (render wil do this anyway on a rebuild as mentioned above). They can be handled with Migrations
- Storing any user data in a database (other than an id from github ). To have users on this system to store any other PII refer to [https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy](https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy) and change the privacy statement.
- Adding extra security [https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application](https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application)
- Testing. There are no tests in this code.
