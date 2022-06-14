from pydantic import BaseModel, Field


class Object(BaseModel):
    id: int = Field(default=None)
    Name: str = Field(...)
    Owner: int = Field(...)
    Data: str = Field()
    ProfilePic: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "Name": "이세계오브젝트",
            }
        }
