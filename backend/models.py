from config import db

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(120), unique = False, nullable = False)
    completed = db.Column(db.Boolean, default = False, nullable = False)

    def to_json(self):
        return {
            "id": self.id,
            "taskName": self.task_name,
            "completed": self.completed
        }