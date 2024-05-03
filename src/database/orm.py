from sqlalchemy import Boolean,Column,Integer,String
from sqlalchemy.orm import declarative_base
from schema.request import CreateTodoRequest

# declarative_base()는 상속 클래스들을 자동으로 인지하고 알아서 매핑해준다. sessionmaker()와 마찬가지로 "클래스"를 리턴해주게 됨.
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

    def done(self) -> "Todo":
        self.is_done = True
        return self

    def undone(self) -> "Todo":
        self.is_done = False
        return self

    def updateContents(self,contents: str) -> "Todo":
        self.contents = contents
        return self