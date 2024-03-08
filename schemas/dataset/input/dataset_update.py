from pydantic import BaseModel
from schemas.dataset.specifications import Specifications


class DatasetUpdate(BaseModel):
    name: str
    description: str | None = None
    specs: Specifications
    oids_add: list[str] | None = None
    oids_delete: list[str] | None = None
    collaborator: str
