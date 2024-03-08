from pydantic import BaseModel


class Specifications(BaseModel):
    det: bool | None = False
    non_det: bool | None = False
    lc: bool | None = False
    xmatch: bool | None = False
    features: list[str] | None = None
    stamps: bool | None = False

    def __getitem__(self, key):
        return getattr(self, key)
