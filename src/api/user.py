
from fastapi import APIRouter,Depends

from database.orm import User
from database.repository import UserRepository
from schema.request import SignUpRequest
from schema.response import UserSchema
from service.user import UserService

router = APIRouter(prefix="/users")

@router.post("/sign-up",status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(UserService),
        user_repo: UserRepository = Depends(UserRepository)) -> UserSchema:

    hash_password = user_service.hash_password(plain_password=request.password)
    user: User = User.create(username=request.username,hashed_password=hash_password)
    create_user = user_repo.create_user(user)
    return UserSchema.from_orm(create_user)

