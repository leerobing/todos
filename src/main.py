from typing import List

from fastapi import FastAPI,Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateTodoRequest
from schema.response import TodoSchema, TodoListSchema

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}

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

@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id : int,
        session: Session = Depends(get_db)
) -> TodoSchema | None:
   todo: Todo | None = get_todo_by_todo_id(session=session,todo_id=todo_id)

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

@app.patch("/todos/{todo_id}")
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(...,embed=True),
        session: Session = Depends(get_db)
) -> TodoSchema:
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        if is_done is True:
            todo.done()
            todo: Todo = update_todo(session=session, todo=todo)
            return TodoSchema.from_orm(todo)
        else:
            todo.undone()
            todo: Todo = update_todo(session=session, todo=todo)
            return TodoSchema.from_orm(todo)

    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)):
    todo: Todo| None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        delete_todo(session=session,todo_id=todo_id)
    raise HTTPException(status_code=404, detail="Todo not found")



