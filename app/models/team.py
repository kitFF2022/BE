from pydantic import BaseModel, Field


class Team(BaseModel):
    id: int = Field(default=None)
    Name: str = Field(...)
    Owner: int = Field(default=None)
    ProfilePic: str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "Name": "홀로라이브",
            }
        }
