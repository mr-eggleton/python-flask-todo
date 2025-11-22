
# Flask Todo App with GitHub & Google OAuth

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![Render](https://img.shields.io/badge/Deploy-Render-purple)

## Features
- Flask + SQLAlchemy ORM
- GitHub & Google OAuth via Flask-Dance
- SQLite (easy to switch to PostgreSQL)
- Ready for Render deployment
- GitHub Actions CI/CD

## GitHub auth setup
Register your app on GitHub Developer Settings:

- Go to [GitHub OAuth Apps](https://github.com/settings/developers) [Full Docs](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app) 
- Create a new OAuth App.
    - You will need one for your dev and you could use this FlaskDance Set up for mulitple sites so id recommend the following set up lot of 


- Set "Application name": FlaskDanceLocalDev
- Set "Homepage URL": http://localhost:5000/
- Set "Application description": For Local FlaskDanceDevelopment
- Set "Authorization callback URL": http://localhost:5000/login/github/callback (for local dev).

![alt text](image.png)

Get Client ID and Client Secret.


## Setup
```bash
git clone <repo-url>
cd flask-todo-oauth
pip install -r requirements.txt
cp .env.example .env
flask run
```

## Deployment on Render
- Add `render.yaml` to repo
- Push to GitHub
- Create Blueprint on Render
- Add environment variables in Render dashboard
