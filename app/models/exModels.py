from pydantic import BaseModel, EmailStr


class resMess(BaseModel):
    message: str


class resSignin(BaseModel):
    access_token: str

class resUserData(BaseModel):
    Name: str
    Team: str
    Nickname: str
    Emailaddr: EmailStr
    ProfilePic: str

class resUser(BaseModel):
    message: resUserData


