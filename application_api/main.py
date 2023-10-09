from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = {}
task_counter = 0

operations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y if y != 0 else None,
}


# Ручка для выполнения операции и получения ID задачи
@app.post("/calculate/")
async def calculate(x: int, y: int, operator: str):
    global task_counter
    task_counter += 1
    task_id = task_counter

    if operator not in operations:
        raise HTTPException(status_code=422, detail="Invalid operator")

    operation = operations[operator]
    result = operation(x, y)

    if result is None:
        raise HTTPException(status_code=422, detail="Division by zero is not allowed")

    tasks[task_id] = {"status": "completed", "result": result}
    return {"task_id": task_id}


# Ручка для получения результата задачи по ID
@app.get("/result/{task_id}")
async def get_result(task_id: int):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=422, detail="Task not found")
    return {"result": task["result"]}


# Ручка для получения списка задач и их статусов
@app.get("/tasks/")
async def get_tasks():
    return tasks
