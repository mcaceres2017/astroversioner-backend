from pydantic import BaseModel
from datetime import date


class DatasetResponse(BaseModel):
    did: int
    name: str
    author: str
    create_date: date
    last_update: date
    last_version: int
