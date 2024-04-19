from fastapi import FastAPI

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
def get_todos_handler(order: str | None = None): # 쿼리 파라미터를 order 혹은 받지 않게 설정
    ret = list(todo_data.values())
    if order and order == 'DESC': # if 문에서 해당 객체에 값이 존재하면 true임
        return ret[::-1] # ::-1 은 해당 리스트를 역정렬함
    return ret