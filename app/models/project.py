from pydantic import BaseModel, Field


class Project(BaseModel):
    id: int = Field(default=None)
    Name: str = Field(...)
    Owner: int = Field(default=None)
    Data: str = Field(default=None)
    ProfilePic: str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "Name": "이세계프로젝트",
            }
        }
