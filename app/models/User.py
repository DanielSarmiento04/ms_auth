from pydantic import BaseModel
from enum import Enum
from typing import Optional

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
    role: Optional[Role] = Role.user

    class Config:
       use_enum_values = True  # <--

class UserInDb(User):
    password:str

