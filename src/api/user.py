from http.client import HTTPException
from typing import List

from fastapi import APIRouter,Depends

from database.orm import User
from database.repository import UserRepository
from schema.request import SignUpRequest, LoginRequest
from schema.response import UserSchema, UserListSchema, JwtResponse
from service.user import UserService

router = APIRouter(prefix="/users")

@router.post("/sign-up",status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(UserService),
        user_repo: UserRepository = Depends(UserRepository)) -> UserSchema:

    hash_password = user_service.hash_password(plain_password=request.password)
    user: User = User.create(username=request.username,password=hash_password)
    create_user = user_repo.create_user(user)
    return UserSchema.from_orm(create_user)

@router.post("/log-in",status_code=200)
def user_log_in_handler(
        request: LoginRequest,
        user_repo: UserRepository = Depends(UserRepository),
        user_service: UserService = Depends(UserService)
):
    user: User | None  = user_repo.get_user_by_username(username=request.username)
    if not user:
        raise HTTPException(status_code=404,detail= "user not found")
    verified : bool = user_service.verify_password(request.password, user.password)
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized" )
    access_token = user_service.create_jwt(username=user.username)

    return JwtResponse(access_token=access_token)

@router.get("/test",status_code=200)
def get_users_handler(user_repo: UserRepository = Depends(UserRepository)) -> UserListSchema:
    users: List[User] = user_repo.get_users()
    return UserListSchema(
        users=[UserSchema.from_orm(user) for user in users]
    )
