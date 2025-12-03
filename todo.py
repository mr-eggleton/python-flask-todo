# todo.py - todo functionality
from flask import Blueprint, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from auth import get_current_user

todo_bp = Blueprint('todo', __name__)
db = SQLAlchemy()

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

@todo_bp.route('/')
def home():
    user = get_current_user()
    if not user:
        return render_template('login.html')
    session['user_id'] = user["id"]
    todos = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', todos=todos, user=user)

@todo_bp.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/')
    task_text = request.form['task']
    new_task = Todo(task=task_text, done=False, user_id=session['user_id'])
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@todo_bp.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        todo.done = not todo.done
        db.session.commit()
    return redirect('/')

@todo_bp.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
