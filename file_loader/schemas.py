from pydantic import BaseModel, Field


class UploadForm(BaseModel):
    first_threshold: int = Field(default=0)
    second_threshold: int = Field(default=0)


class DownloadForm(BaseModel):
    file_name: str
