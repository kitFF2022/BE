from pydantic import BaseModel


class resMess(BaseModel):
    message: str


class resSignin(BaseModel):
    access_token: str
