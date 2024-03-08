from pydantic import BaseModel


class MetadataResponse(BaseModel):
    name: str
    versions: list[int]
    description: str | None = None
    create_date: str
    author: str
    parent_did: int | None = None
    parent_did_name: str | None = None
