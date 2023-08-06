from typing import Optional
from pydantic import BaseModel


class Hoax(BaseModel):
    content: str
    status: str
    article_link: Optional[str] = None
