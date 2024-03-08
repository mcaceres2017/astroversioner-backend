from pydantic import BaseModel
from schemas.dataset.specifications import Specifications


class DatasetInformation(BaseModel):
    name: str
    author: str
    description: str | None = None
    parent_did: int | None = None
    oids: list[str]
    specs: Specifications
