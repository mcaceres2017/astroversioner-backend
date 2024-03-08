from pydantic import BaseModel
from schemas.dataset.specifications import Specifications


class VersionResponse(BaseModel):
    collaborator: str
    version_date: str
    specs: Specifications
    oids: list[str]
