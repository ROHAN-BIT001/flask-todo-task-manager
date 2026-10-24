from flask import Flask, request

app = Flask(__name__)

tasks = []   # each task is a dictionary: {"id": 1, "title": "...", "done": False}
next_id = 1


@app.route("/")
def home():
    return "Welcome to the To-Do Task Manager!"


@app.route("/tasks")
def show_tasks():
    if len(tasks) == 0:
        return "No tasks yet. Add one using the /add route."
    lines = []
    for t in tasks:
        status = "Done" if t["done"] else "Pending"
        lines.append(f"{t['id']}. {t['title']} - {status}")
    return " , ".join(lines)


@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("title", "").strip()

    # Input validation
    if title == "":
        return "Error: Please enter a task title. It cannot be empty.", 400
    if len(title) > 100:
        return "Error: Task title is too long (max 100 characters).", 400

    tasks.append({"id": next_id, "title": title, "done": False})
    next_id += 1
    pending = len([t for t in tasks if not t["done"]])
    return f"Task '{title}' added! You have {pending} pending task(s)."


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            return f"Task '{t['title']}' marked as done!"
    return "Error: Task not found.", 404


if __name__ == "__main__":
    app.run(debug=True)
