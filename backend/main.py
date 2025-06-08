from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# create database 
load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] =  os.getenv("DATABASE_URI", "sqlite:///local.db") # fetch DB URI from .env file and resorts to local.db if DB URI is not in env file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False, unique=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)

    def to_dict(self):
        return {
            "id" : self.id,
            "task" : self.task,
            "completed" : self.completed
        }
    
with app.app_context():
    db.create_all()

# create routes 
@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "API is running"}), 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = ToDo.query.all() # fetch every row in the database
    return jsonify([task.to_dict() for task in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = ToDo(task=data["task"])
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message" : f'"{new_task.task}"has been added successfully!'}), 201

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    task = ToDo.query.get(task_id)

    if not task:
        return jsonify({"error" : "Task not found!"}), 404

    data = request.get_json()
    if "completed" in data:
        task.completed = data["completed"]
    else:
        task.completed = not task.completed
    db.session.commit()
    return jsonify(task.to_dict())

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = ToDo.query.get(task_id)

    if not task:
        return jsonify({"error" : "Task not found!"}), 404
    
    db.session.delete(task)
    db.session.commit() 
    return jsonify({"message" : "Task deleted!"})



if __name__ == "__main__":
    app.run(debug=True)
