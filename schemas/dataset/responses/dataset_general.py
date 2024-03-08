from pydantic import BaseModel
from datetime import date


class DatasetGeneralInformation(BaseModel):
    did: int | None = None
    name: str | None = None
    version: int | None = None
    author: str | None = None
