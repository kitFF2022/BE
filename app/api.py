from os import access
from fastapi import FastAPI, status, Body, Depends, File, Header, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.auth.auth_bearer import JWTBearer
from app.db import DB
from app.models.user import User, UserSignIn
from app.models.exModels import resMess, resSignin, resUser
from app.auth.auth_handler import signJWT, decodeJWT
from typing import Optional
import shutil

app = FastAPI(debug=False)
mydb = DB()

origins = ["http://localhost", "http://localhost:3000",
           "http://localhost:8000", "http://localhost:8080",
           "https://localhost", "https://localhost:3000",
           "https://localhost:8000", "https://localhost:8080",
           "localhost", "localhost:3000",
           "localhost:8000", "localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', "DELETE", 'OPTIONS'],
    allow_headers=['*'],
)


@app.get("/", tags=["root"], response_model=resMess)
async def read_root() -> dict:
    item = {"message": "WORKING !!!"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)


@app.post("/user/signin", tags=["user"], response_model=resSignin)
async def user_signin(user: UserSignIn = Body(...)):
    res = mydb.signinUser(user)
    if res == 1:
        return signJWT(user.Emailaddr)
    elif res == 2:
        item = {
            "message": "Signin Failed"
        }
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        item = {
            "message": "DB might be dead T.T"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


@app.post("/user/signup", tags=["user"], response_model=resMess)
async def user_signup(user: User = Body(...)):
    res = mydb.signupUser(user)
    if res == 1:
        item = {
            "message": "Signup Success"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    elif res == 2:
        item = {
            "message": "That Emailaddr already exist"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)
    else:
        item = {
            "message": "DB might be dead T.T"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


@app.post("/user/profilePic", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_profilePic(file: UploadFile, Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    f = open("c:/profilepic/" + file.filename, 'wb')
    print(file.filename)
    shutil.copyfileobj(file.file, f)
    f.close()
    print(decoded["Emailaddr"])
    item = {
        "message": "file uploaded but not committed to DB"
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)

@app.get("/user/userData", dependencies=[Depends(JWTBearer())], tags=["user"], response_model=resUser)
async def user_getUserData(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbUser = mydb.getUserData(decoded["Emailaddr"])
    #dbUser 확인하여 에러 처리 필요
    item = {
        "message": dbUser
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)


@app.get("/TEST/DB/DROPTABLE", tags=["TEST"], response_model=resMess)
async def test_DropTable():
    if mydb.WarnTestDelAllTableData():
        item = {
            "message": "All tables DROPED and CREATED"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        item = {
            "message": "Internal server error"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)
