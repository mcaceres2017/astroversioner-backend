from pydantic import BaseModel
from datetime import date
from schemas.dataset.responses.dataset_general import DatasetGeneralInformation


class DatasetCreationResponse(BaseModel):
    success: bool
    message: str
    dataset: DatasetGeneralInformation | None = None
