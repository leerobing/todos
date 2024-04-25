from typing import List

from fastapi import FastAPI,Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos, get_todo_by_todo_id, create_todo
from schema.request import CreateTodoRequest
from schema.response import TodoSchema, TodoListSchema

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}


todo_data = {
    1 : {
        "id" : 1,
        "contents": "실전! FastAPi 챕터 0 수강",
        "is_done": True
    },
    2 : {
        "id" : 2,
        "contents": "실전! FastAPi 챕터 0 수강",
        "is_done": False
    },
    3: {
        "id" : 3,
        "contents": "실전! FastAPi 챕터 0 수강",
        "is_done": False
    },
    4: {
        "id" : 4,
        "contents": "실전! FastAPi 챕터 0 수강",
        "is_done": True
    }
}
@app.get("/todos")
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
) -> TodoListSchema: # 쿼리 파라미터를 order 혹은 받지 않게 설정

    todos: List[Todo] = get_todos(session=session)

    if order and order == 'DESC': # if 문에서 해당 객체에 값이 존재하면 true임
         return TodoListSchema(
            todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]]  # ::-1 은 해당 리스트를 역정렬함
    )
    return TodoListSchema(
        todos=[TodoSchema.from_orm(todo) for todo in todos]
    )

@app.get("/todos/{todos_id}", status_code=200)
def get_todo_handler(
        todos_id : int,
        session: Session = Depends(get_db)
) -> TodoSchema | None:
   todo: Todo | None = get_todo_by_todo_id(session=session,todo_id=todos_id)

   if todo:
        return TodoSchema.from_orm(todo)
   raise HTTPException(status_code=404,detail="Todo not found")

@app.post("/todos", status_code=201)
def post_todo_hanlder(
        request: CreateTodoRequest,
        session: Session = Depends(get_db)
) -> TodoSchema:
    todo: Todo = Todo.create(request=request)
    todo: Todo = create_todo(session=session, todo=todo)
    return TodoSchema.from_orm(todo)

@app.patch("/todos/{todos_id}")
def update_todo_handler(
        todos_id : int,
        is_done : bool = Body(...,embed=True),
        session: Session = Depends(get_db)
):
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todos_id)
    if todo:
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todos_id}", status_code=204)
def delete_todo_handler(todos_id: int):
    todo = todo_data.get(todos_id)
    if todo:
        todo_data.pop(todos_id, None)
        return
    raise HTTPException(status_code=404, detail="Todo not found")



