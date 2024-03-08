from pydantic import BaseModel
from schemas.dataset.specifications import Specifications


class UpdateInformation(BaseModel):
    did: int | None = None
    name: str | None = None
    description: str | None = None
    old_version: int | None = None
    new_version: int | None = None
    specs: Specifications | None = None
    added_oids: list[str] | None = None
    deleted_oids: list[str] | None = None
