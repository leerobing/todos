from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
from database.orm import Todo


def get_todos(session : Session) -> List[Todo]:
    return list(session.scalars(select(Todo)))

def get_todo_by_todo_id(session : Session, todo_id : int) -> Todo | None:
    return session.scalar(select(Todo).where(Todo.id == todo_id))
def create_todo(session : Session, todo : Todo) -> Todo:
    session.add(instance=todo) # 세션 객체에 db에 저장하고자 하는 객체를 저장한다.
    session.commit() # 이시점에서 db에 반영된다.
    session.refresh(instance=todo) #pk id 값이 할당된 todo 객체를 read 한다.
    return todo