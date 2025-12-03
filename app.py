
import os
from flask import Flask
from auth import auth_bp
from todo import todo_bp, init_app as init_todo

SITE = {
    "WebsiteName": "TodoApp",
    "ControllerName": "UTC Sheffield Olympic Legacy Park",
    "ControllerAddress": "UTC Sheffield Olympic Legacy Park, 2 Old Hall Road, Sheffield, S9 3TU",
    "ControllerURL": "https://www.utcsheffield.org.uk/olp/",
}

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "supersecret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(todo_bp)

@app.context_processor
def inject_dict_for_all_templates():
    return {"site": SITE}

# Initialize todo module (db and tables)
init_todo(app)

if __name__ == '__main__':
    app.run(debug=True)
