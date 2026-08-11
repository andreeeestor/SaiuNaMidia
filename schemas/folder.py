from pydantic import BaseModel


class FolderItem(BaseModel):
    name: str
    path: str


class CreateFolderRequest(BaseModel):
    path: str


class CreateFolderResponse(BaseModel):
    success: bool
    path: str
