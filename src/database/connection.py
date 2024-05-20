from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#데이터 베이스 연결을 위한 url/ 로컬에 mysql이 설치되어 있기 때문에 호스트 포트를 3305로 변경하였다.
DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3305/todos"

#echo 는 쿼리 동작시 sql 쿼리를 출력해주는 옵션
engine = create_engine(DATABASE_URL)

#session 객체를 만들기 위한 session factory 객체
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()