from typing import ClassVar
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

    class Config: 
        json_schema_extra = {
            "example": {
                "email": "nurudeen@gmail.com",
                "password": "password"
            }
        }
        

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:  
        json_schema_extra = {
            "example": {
                "email": "nurudeen@gmail.com",
                "password": "password"
            }
        }
