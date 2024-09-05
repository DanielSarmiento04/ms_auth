from pydantic import BaseModel
from enum import Enum

class User(BaseModel):
    username:str

class UserInDb(User):
    password:str

    