from typing import List

from sqlalchemy import select, delete
from fastapi import Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.orm import User

class TodoRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_todos(self) -> List[Todo]:
        return list(self.session.scalars(select(Todo)))

    def get_todo_by_todo_id(self, todo_id : int) -> Todo | None:
        return self.session.scalar(select(Todo).where(Todo.id == todo_id))
    def create_todo(self, todo : Todo) -> Todo:
        self.session.add(instance=todo) # 세션 객체에 db에 저장하고자 하는 객체를 저장한다.
        self.session.commit() # 이시점에서 db에 반영된다.
        self.session.refresh(instance=todo) #pk id 값이 할당된 todo 객체를 read 한다.
        return todo
    def update_todo(self, todo : Todo) -> Todo:
        self.session.add(instance=todo)
        self.session.commit()
        self.session.refresh(instance=todo)
        return todo

    def delete_todo(self, todo_id : int) -> None:
        self.session.execute(delete(Todo).where(Todo.id == todo_id))
        self.session.commit()


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user

    def get_users(self) -> List[User]:
        return list(self.session.scalars(select(User)).unique())

