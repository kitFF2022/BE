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
    Position: List[float]
    Rotation: List[float]
    Scale: List[float]

    class Config:
        schema_extra = {
            "example": {
                "Position": [0.0, 0.0, 0.0],
                "Rotation": [0.0, 0.0, 0.0],
                "Scale": [0.0, 0.0, 0.0]
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
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    }
                ]
            }
        }


# objectId -> 0: shelf, 1: boiler, 2: waterTank, 3: CO2tank
class ProjectObject(BaseModel):
    objectId: int
    Position: List[float]
    Rotation: List[float]
    Scale: List[float]

    class Config:
        schema_extra = {
            "example": {
                "objectId": 0,
                "Position": [0.0, 0.0, 0.0],
                "Rotation": [0.0, 0.0, 0.0],
                "Scale": [0.0, 0.0, 0.0]
            }
        }


class ProjectObjData(BaseModel):
    ObjectCount: int
    Objects: List[ProjectObject]

    class Config:
        schema_extra = {
            "example": {
                "ObjectCount": 4,
                "Objects": [
                    {
                        "objectId": 0,
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "objectId": 1,
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "objectId": 2,
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    },
                    {
                        "objectId": 3,
                        "Position": [0.0, 0.0, 0.0],
                        "Rotation": [0.0, 0.0, 0.0],
                        "Scale": [0.0, 0.0, 0.0]
                    }
                ]
            }
        }
