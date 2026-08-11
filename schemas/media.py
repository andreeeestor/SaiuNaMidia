from pydantic import BaseModel


class ImageItem(BaseModel):
    key: str
    url: str
    name: str
    size: int
    uploadedAt: str


class DeleteImageRequest(BaseModel):
    key: str


class MoveImageRequest(BaseModel):
    key: str
    targetFolder: str


class ActionResponse(BaseModel):
    success: bool
