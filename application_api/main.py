from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = {}
task_counter = 0

operations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y if y != 0 else None,
}


class CalculationRequest(BaseModel):
    x: int
    y: int
    operator: str


@app.post("/calculate/")
async def calculate(request_data: CalculationRequest):
    global task_counter
    task_counter += 1
    task_id = task_counter

    if request_data.operator not in operations:
        raise HTTPException(status_code=422, detail="Invalid operator")

    operation = operations[request_data.operator]
    result = operation(request_data.x, request_data.y)

    if result is None:
        raise HTTPException(status_code=422, detail="Division by zero is not allowed")

    tasks[task_id] = {"status": "completed", "result": result}
    return {"task_id": task_id}


@app.get("/result/{task_id}")
async def get_result(task_id: int):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=422, detail="Task not found")
    return {"result": task["result"]}


@app.get("/tasks/")
async def get_tasks():
    return tasks
