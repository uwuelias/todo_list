import React from "react";

const ToDoItem = ({ task, onToggle, onDelete }) => {
  return (
    <div className="flex flex-row gap-2">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggle(task.id, !task.completed)}
      />
      <span>{task.task}</span>
      <button>delete</button>
    </div>
  );
};

export default ToDoItem;
