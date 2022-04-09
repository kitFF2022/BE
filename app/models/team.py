from pydantic import BaseModel, Field


class Team(BaseModel):
    id: int = Field(default=None)
    Name: str = Field(...)
    Owner: int = Field(...)
    ProfilePic: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "Name": "홀로라이브",
            }
        }
