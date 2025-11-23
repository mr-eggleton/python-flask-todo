import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_dance.contrib.github import make_github_blueprint, github

SITE={
        "WebsiteName": "TodoApp",
        "ControllerName": "UTC Sheffield Olympic Legacy Park",
        "ControllerAddress": "UTC Sheffield Olympic Legacy Park, 2 Old Hall Road, Sheffield, S9 3TU",
        "ControllerURL": "https://www.utcsheffield.org.uk/olp/",
        }
    
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "supersecret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# OAuth Blueprints
github_bp = make_github_blueprint(client_id=os.getenv("GITHUB_CLIENT_ID"), client_secret=os.getenv("GITHUB_CLIENT_SECRET"))
app.register_blueprint(github_bp, url_prefix="/login")

@app.context_processor
def inject_dict_for_all_templates():
    return {"site": SITE}

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
        if "github" in session:
            data = session["github"]
        else:
            response = github.get("/user")
            session["github"] = response.json()
            data = session["github"]
        return {"id": str(data["id"]), "name": data["login"]}
    return None

@app.route('/')
def home():
    user = get_current_user()
    if not user:
        return render_template('login.html')
    session['user_id'] = user["id"]
    todos = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', todos=todos, user=user)

@app.route('/privacy')
def privacy():
    user = get_current_user()
    return render_template('privacy.html', user=user)

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

with app.app_context():
    create_tables()

if __name__ == '__main__':
    app.run(debug=True)
