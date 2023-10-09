from fastapi.testclient import TestClient

from application_api.main import app, tasks

client = TestClient(app)


# Ваши тесты
def test_calculate_valid():
    response = client.post("/calculate/", json={"x": 5, "y": 3, "operator": "+"})
    assert response.status_code == 200


def test_calculate_invalid_operator():
    response = client.post("/calculate/", json={"x": 5, "y": 3, "operator": "invalid"})
    assert response.status_code == 422


def test_calculate_division_by_zero():
    response = client.post("/calculate/", json={"x": 5, "y": 0, "operator": "/"})
    assert response.status_code == 422


def test_get_result_valid_task():
    task_id = 1
    tasks[task_id] = {"status": "completed", "result": 8}
    response = client.get(f"/result/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert "result" in data


def test_get_result_invalid_task():
    response = client.get("/result/999")
    assert response.status_code == 422
    assert "detail" in response.json()
