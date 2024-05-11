from database.orm import User
from database.repository import UserRepository

def test_user_sign_up_api(client,mocker):
    mocker.patch.object(
        UserRepository,"create_user",
        return_value=User(id=1, username="test", password="<PASSWORD>"))

    body = {"username": "test","password": "<PASSWORD>"}
    response = client.post("/users/sign-up", json=body)

    assert response.status_code == 201

