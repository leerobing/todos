from fastapi import FastAPI
from api import todo

app = FastAPI() #app은 FastAPI의 인스턴스를 참조하는 변수
app.include_router(todo.router)# app에 router를 연결해준다.

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}



