from datetime import datetime,timedelta

import bcrypt
from jose import jwt

class UserService:

    encoding: str = "UTF-8"
    secret_key: str = "cd74e4d0c346a47bdc760ce0a8b0c3d134ba5e7eacb667fbfdb72159fe19e662"
    jwt_algorithm : str = "HS256"
    def hash_password(self, plain_password: str) -> str:
        hashed_password = bcrypt.hashpw(plain_password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
       return bcrypt.checkpw(plain_password.encode(self.encoding),hashed_password.encode(self.encoding))

    def create_jwt(self, username: dict) -> str:
        return jwt.encode(
            {"sub" : username,"exp":datetime.now() + timedelta(days=1)},
            self.secret_key,
             algorithm= self.jwt_algorithm)