from pydantic import BaseModel

class User(BaseModel):
    mail: str
    username: str
    password: str