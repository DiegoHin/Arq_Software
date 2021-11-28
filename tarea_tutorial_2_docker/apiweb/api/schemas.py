from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date

class news(BaseModel):
    id: int
    url: str
    title: str
    date: date
    media_outlet: str
    category: str

    class Config:
        orm_mode = True
        allow_mutation = True