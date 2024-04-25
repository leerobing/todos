from sqlalchemy import Boolean,Column,Integer,String
from sqlalchemy.orm import declarative_base

from schema.request import CreateTodoRequest

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False )
    is_done = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"Todo(id={self.id},contents={self.contents},is_done={self.is_done}))"

    # Pydantic 객체를 ORM 객체로 변환하기 위한 클레스 메서드
    @classmethod
    def create(cls, request : CreateTodoRequest) -> "Todo":
        return cls(
            contents=request.contents,
            is_done=request.is_done
        )

