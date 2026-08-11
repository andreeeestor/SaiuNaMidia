from typing import Optional, List
from pydantic import BaseModel


class ExtractMediaRequest(BaseModel):
    url: str


class ExtractMediaResponse(BaseModel):
    url: str
    title: Optional[str] = None
    summary: Optional[str] = None
    image: Optional[str] = None
    logo: Optional[str] = None
    portal_name: Optional[str] = None


class NewsArticleItem(BaseModel):
    title: str
    summary: str
    url: str
    image: Optional[str] = ""
    logo: Optional[str] = ""
    portal_name: Optional[str] = "Saiu na Mídia"


class GenerateNewsletterRequest(BaseModel):
    articles: List[NewsArticleItem]
    date_header: Optional[str] = None


class GenerateNewsletterResponse(BaseModel):
    email_html: str
    wcm_html: str
