from typing import Optional
from pydantic import BaseModel


class ExtractMediaRequest(BaseModel):
    url: str


class ExtractMediaResponse(BaseModel):
    url: str
    title: Optional[str] = None
    image: Optional[str] = None
    logo: Optional[str] = None
