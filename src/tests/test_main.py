from database.orm import Todo
from database.repository import TodoRepository


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping":"pong"}

def test_get_todos(client,mocker): #pytestFixture 적용
    mocker.patch.object(TodoRepository,"get_todos", return_value=[
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

def test_get_todo_by_todo_id(client,mocker):

    #200
    mocker.patch.object(TodoRepository,
        "get_todo_by_todo_id",
        return_value=Todo(id=1, contents="FastAPI Section 0",is_done=False))

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, "contents": "FastAPI Section 0","is_done": False
    }

    #404
    mocker.patch.object(TodoRepository,
        "get_todo_by_todo_id", return_value=None)
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Todo not found"
    }

def test_post_todo(client,mocker):
    mocker.patch.object(TodoRepository,
        "create_todo",
        return_value=Todo(id=1, contents="todo", is_done=True))

    # Todo 클래스의 create 메서드를 spy한다. mocking을 사용하다 보면 요청 값과 검증 대상 로직의 결과값이 다를 수 있다.
    #  그럴땐 요청 값을 잘 처리하는지 확인이 필요한데 이때 사용하는 것이 spy다.

    create_spy = mocker.spy(Todo, "create")
    body = {"contents": "test","is_done":True}
    response = client.post("/todos",json=body)

    assert create_spy.spy_return.id is None # spy_return 이라는 속성을 통해 해당 request를 잘 처리 했는지 확인할 수 있다.
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is True

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "contents": "todo",
        "is_done": True
    }
def test_patch_todo(client, mocker):

    #200
    mocker.patch.object(TodoRepository,
        "get_todo_by_todo_id",
        return_value=Todo(id=1, contents="todo",is_done=False)
    )
    done = mocker.patch.object(Todo, "done")
    mocker.patch.object(TodoRepository,
        "update_todo",
        return_value=Todo(id=1, contents="todo",is_done=True)
    )

    response = client.patch("/todos/1", json={"is_done":True})
    done.assert_called_once_with()
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "contents": "todo",
        "is_done": True
    }

    #404
    mocker.patch.object(TodoRepository,
       "get_todo_by_todo_id",
        return_value=None
    )
    response = client.get("/todos/3")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Todo not found"
    }

# def test_delete_todo_success(client, mocker):
#     # 200
#     mocker.patch(
#         "api.todo.get_todo_by_todo_id",
#         return_value=Todo(id=1, contents="FastAPI Section 0", is_done=False))
#
#     # Performing the DELETE request
#     response = client.delete("/todos/1")
#
#     # Assertions
#     assert response.status_code == 204
#     assert response.text == ""
#
#     # mocker.patch(
#     #     "api.todo.get_todo_by_todo_id", return_value=None)
#     # response = client.delete("/todos/1")
#     # assert response.status_code == 404
#     # assert response.json() == {
#     #     "detail": "Todo not found"
#     # }
#     #
#
#
#

