from typing import List

from fastapi import Depends, HTTPException, Body, APIRouter
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo, User
from database.repository import TodoRepository, UserRepository
from schema.request import CreateTodoRequest
from schema.response import TodoListSchema, TodoSchema
from security import get_access_token
from service.user import UserService

router = APIRouter(prefix="/todos") #router를 통해 요청을 받음, prefix는 @RequestMapping 같이 고정 url를 지정할 수 있음
@router.get("")
def get_todos_handler(
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repo : UserRepository = Depends( ),
    order: str | None = None,
    todo_rpo: TodoRepository = Depends(TodoRepository)
) -> TodoListSchema: # 쿼리 파라미터를 order 혹은 받지 않게 설정

    print("----------------------")
    print(access_token)
    print("----------------------")
    
    username= user_service.decode_jwt(access_token=access_token)
    user: User = user_repo.get_user_by_username(username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    todos: List[Todo] = user.todos

    if order and order == 'DESC': # if 문에서 해당 객체에 값이 존재하면 true임
         return TodoListSchema(
            todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]]  # ::-1 은 해당 리스트를 역정렬함
    )
    return TodoListSchema(
        todos=[TodoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id : int,
        todo_repo: TodoRepository = Depends(TodoRepository)
) -> TodoSchema | None:
   todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)

   if todo:
        return TodoSchema.from_orm(todo)
   raise HTTPException(status_code=404,detail="Todo not found")


@router.post("", status_code=201)
def post_todo_hanlder(
        request: CreateTodoRequest,
        todo_repo : TodoRepository = Depends(TodoRepository)
) -> TodoSchema:
    todo: Todo = Todo.create(request=request)
    todo: Todo = todo_repo.create_todo(todo=todo)
    return TodoSchema.from_orm(todo)


@router.patch("/{todo_id}")
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(...,embed=True),
        todo_repo: TodoRepository = Depends(TodoRepository)
) -> TodoSchema:
    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        if is_done is True:
            todo.done()
            todo: Todo = todo_repo.update_todo(todo=todo)
            return TodoSchema.from_orm(todo)
        else:
            todo.undone()
            todo: Todo = todo_repo.update_todo(todo=todo)
            return TodoSchema.from_orm(todo)

    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        todo_repo: TodoRepository = Depends(TodoRepository)):

    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)

    if todo:
        todo_repo.delete_todo( todo_id=todo_id)

    raise HTTPException(status_code=404, detail="Todo not found")
