from pydantic import BaseModel, Field
from typing import List


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


class Wall(BaseModel):
    Front: List[int]
    length: int

    class Config:
        schema_extra = {
            "example": {
                "Front": [0.0, 0.0, 0.0],
                "length": 10
            }
        }


class ProjectData(BaseModel):
    WallCount: int
    Walls: List[Wall]

    class Config:
        schema_extra = {
            "example": {
                "WallCount": 4,
                "Walls": [
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "length": 10
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "length": 10
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "length": 10
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "length": 10
                    }
                ]
            }
        }
