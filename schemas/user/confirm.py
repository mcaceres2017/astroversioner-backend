from pydantic import BaseModel
from schemas.user.user import User


class Confirm(BaseModel):
    response: bool
    user: User
    detail: str
