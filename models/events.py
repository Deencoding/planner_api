from pydantic import BaseModel
from typing import ClassVar, List

class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str] 
    location: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Nurudeen's Birthday",
                "image": "https://linktomyimage.com/image.png",
                "description": "we will be giving out gifts to the celebrant!",
                "tags": ["birthday", "age", "year", "month"],
                "location": "Sheraton Hotel"
            }
        }
class EventUpdate(BaseModel):
    id: int
    title: str | None
    image: str | None 
    description: str | None 
    tags: List[str] | None
    location: str | None  
    
    class config: 
        json_schema_extra = {
            "example": {
                "title": "Nurudeen's Birthday",
                "image": "https://linktomyimage.com/image.png",
                "description": "we will be giving out gifts to the celebrant!",
                "tags": ["birthday", "age", "year", "month"],
                "location": "Sheraton Hotel"
            }
        }