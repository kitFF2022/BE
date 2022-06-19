from re import L
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
    Front: List[float]
    Length: int

    class Config:
        schema_extra = {
            "example": {
                "Front": [0.0, 0.0, 0.0],
                "Length": 10
            }
        }


class ProjectWallData(BaseModel):
    WallCount: int
    Walls: List[Wall]

    class Config:
        schema_extra = {
            "example": {
                "WallCount": 4,
                "Walls": [
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Length": 10
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Length": 10
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Length": 10
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Length": 10
                    }
                ]
            }
        }


class Object(BaseModel):
    Front: List[float]
    Scale: List[float]

    class Config:
        schema_extra = {
            "example": {
                "Front": [0.0, 0.0, 0.0],
                "Scale": [0.0, 0.0, 0.0]
            }
        }


class ProjectObjData(BaseModel):
    ObjectCount: int
    Objects: List[Object]

    class Config:
        schema_extra = {
            "example": {
                "ObjectCount": 4,
                "Objects": [
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "Front": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    }
                ]
            }
        }
