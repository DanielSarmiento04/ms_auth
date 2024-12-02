from pydantic import BaseModel
from enum import Enum

class Operator(
    BaseModel
):
    '''
        This is the Operator model
            
    '''


class Role(Enum):
    admin = 'admin'
    user = 'user'

class User(BaseModel):
    username:str
    role: Role  = Role.user


    class Config:
       use_enum_values = True  # <--

class UserInDb(User):
    password:str

