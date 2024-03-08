from pydantic import BaseModel
from schemas.dataset.responses.update_information import UpdateInformation


class DatasetUpdateResponse(BaseModel):
    success: bool
    message: str
    updated_dataset: UpdateInformation | None = None
