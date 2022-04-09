from email.policy import default
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int = Field(default=None)
    Name: str = Field(...)
    Team: str = Field(...)
    Nickname: str = Field(...)
    Emailaddr: EmailStr = Field(...)
    Password: str = Field(...)
    ProfilePic: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "Name": "시로가네 노엘",
                "Nickname": "카난",
                "Emailaddr": "canan8181@gmail.com",
                "Password": "SuperPowerfulPW",
            }
        }
