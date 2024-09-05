from pydantic import BaseModel
from enum import Enum

class State(str, Enum):
    Active = "Active"
    Disable = "Disable"

class Role(str, Enum):
    Website = "Website"
    Mobile = "Mobile"
    Desktop = "Desktop"



class Client(BaseModel):
    client_id: str
    state: State = State.Active
    role: Role

    class Config:
       use_enum_values = True  # <--
    

class ClientInDB(Client):
    password: str
