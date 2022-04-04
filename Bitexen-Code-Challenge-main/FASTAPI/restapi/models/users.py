from pydantic import BaseModel

class User(BaseModel):
    mail:str = None
    name_surname:str = None
    password:str = None