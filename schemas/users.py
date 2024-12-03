from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "nurudeen@gmail.com",
                "password": "StrongPassword123!"
            }
        }


class UserCreate(UserBase):
    pass


class UserSignIn(UserBase):
    pass
