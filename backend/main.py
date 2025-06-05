from flask import request, jsonify
from config import app, db
from models import ToDo

@app.route("/todo_list", methods = ["GET"])
def get_todo_List():
    list = ToDo.query.all()
    json_list = list(map(lambda x : x.to_json(), list))
    return jsonify({"todo_list": json_list})

@app.route("create_task", methods = ["POST"])
def create_task():
    task = request.json.get("task")
    completed = request.json.get("completed")

    if not task or not completed:
        return jsonify({"message" : "You must include a task"}), 400
    
    new_task = ToDo(task_name = task, completed = False)
    try:
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        return jsonify({"message" : str(e)}), 400
    
    return jsonify({"message" : "task added successfully!"}), 201

@app.route("/update_task/<int:task_id>", methods = ["PATCH"])
def update_task(task_id):
    task = ToDo.query.get(task_id)

    if not task:
        return jsonify({"message" : "task not found!"}), 404
    
    data = request.json
    task.task_name = data.get("task", task.task_name)
                
    db.session.commit()

    return jsonify({"message" : "task updated"}), 200

if __name__ == "__main__":
    with app.app_context:
        db.create_all()

    app.run(debug = True)