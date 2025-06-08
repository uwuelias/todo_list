import React, { useState, useEffect } from "react";
import API from "../api";
import ToDoItem from "./ToDoItem";

const ToDoList = () => {
  const [taskList, setTaskList] = useState([]);
  const [newTask, setNewTask] = useState("");

  const fetchTasks = async () => {
    const response = await API.get("/tasks");
    setTaskList(response.data);
  };

  const addTask = async () => {
    if (!newTask.trim()) return;
    await API.post("/tasks", { task: newTask });
    setNewTask("");
    fetchTasks();
  };

  const toggleTask = async (id, completed) => {
    await API.patch(`/tasks/${id}`, { completed });
    fetchTasks();
  };

  const deleteTask = async (id, completed) => {
    await API.delete(`/tasks/${id}`);
    fetchTasks;
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="flex flex-col items-center">
      <h2 className="text-black">Todo List</h2>
      <div className="">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Add new task"
        />
        <button onClick={addTask}>Add</button>
      </div>
      {taskList.map((task) => (
        <ToDoItem key={task.id} task={task} onToggle={toggleTask} />
      ))}
    </div>
  );
};

export default ToDoList;
