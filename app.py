
import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "supersecret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# OAuth Blueprints
github_bp = make_github_blueprint(client_id=os.getenv("GITHUB_CLIENT_ID"), client_secret=os.getenv("GITHUB_CLIENT_SECRET"))
app.register_blueprint(github_bp, url_prefix="/login")
# google_bp = make_google_blueprint(client_id=os.getenv("GOOGLE_CLIENT_ID"), client_secret=os.getenv("GOOGLE_CLIENT_SECRET"), scope=["profile", "email"])
# app.register_blueprint(google_bp, url_prefix="/login")

@dataclass
class Todo(db.Model):
    id: int
    task: str
    done: bool
    user_id: str

    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(100), nullable=False)

def create_tables():
    db.create_all()

def get_current_user():
    if github.authorized:
        resp = github.get("/user")
        return {"id": str(resp.json()["id"]), "name": resp.json()["login"]}
    # elif google.authorized:
    #     resp = google.get("/oauth2/v2/userinfo")
    #     return {"id": str(resp.json()["id"]), "name": resp.json()["name"]}
    return None

@app.route('/')
def home():
    user = get_current_user()
    if not user:
        return render_template('login.html')
    session['user_id'] = user["id"]
    todos = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', todos=todos, user=user)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/')
    task_text = request.form['task']
    new_task = Todo(task=task_text, done=False, user_id=session['user_id'])
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        todo.done = not todo.done
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        create_tables()

    app.run(debug=True)
