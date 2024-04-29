from fastapi.testclient import TestClient

from database.orm import Todo
from main import app


client = TestClient(app=app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping":"pong"}


def test_get_todos(mocker):
    mocker.patch("main.get_todos", return_value=[
        Todo(id=1, contents="FastAPI Section 0",is_done=False),
        Todo(id=2, contents="FastAPI Section 1", is_done=True),
    ])
    # mocker를 통해 가상의 디비를 만들어 코드를 테스트 한다.
    # 해당 테스트 코드가 어떤 함수의 실행을 테스트 하는 것인지 mocker.patch()를 통해 명시한다.
    # return_value 설정으로 반환값을 지정할 수 있다.

    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {"todos": [
        {"id": 1,"contents": "FastAPI Section 0","is_done": False},
        {"id": 2,"contents": "FastAPI Section 1","is_done": True}
    ]}

    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {"todos": [
        {"id": 2, "contents": "FastAPI Section 1", "is_done": True},
        {"id": 1, "contents": "FastAPI Section 0", "is_done": False}

    ]}
