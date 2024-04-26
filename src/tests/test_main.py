from fastapi.testclient import TestClient

from main import app


client = TestClient(app=app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping":"pong"}


def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {"todos": [
        {"id": 1,"contents": "FastAPI Section 0","is_done": True},
        {"id": 2,"contents": "FastAPI Section 1","is_done": True},
        {"id": 5, "contents": "FastAPI Section 55", "is_done": True}
    ]}

    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {"todos": [
        {"id": 5, "contents": "FastAPI Section 55", "is_done": True},
        {"id": 2, "contents": "FastAPI Section 1", "is_done": True},
        {"id": 1, "contents": "FastAPI Section 0", "is_done": True}
    ]}
