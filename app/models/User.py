from pydantic import BaseModel
from enum import Enum

class Role(Enum):
    admin = 'admin'
    user = 'user'

class User(BaseModel):
    username:str
    role:Role  = Role.user.value

class UserInDb(User):
    password:str

