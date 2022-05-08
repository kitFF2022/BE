from os import access
from fastapi import FastAPI, status, Body, Depends, File, Header, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from app.auth.auth_bearer import JWTBearer
from app.db import DB
from app.models.user import User, UserSignIn, UserUpdate
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
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
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
async def user_PostProfilePic(file: UploadFile, Authorization: Optional[str] = Header(None)):
    ext = ["jpg", "JPG", "PNG", "png"]
    token = Authorization[7:]
    decoded = decodeJWT(token)
    filename = file.filename.split('.')
    if filename[len(filename) - 1] in ext:
        filename = decoded["Emailaddr"] + "." + filename[len(filename) - 1]
        f = open("./imgs/" + filename, 'wb')
        shutil.copyfileobj(file.file, f)
        f.close()
        mydb.updateUserProfilePic(filename, decoded["Emailaddr"])
        item = {
            "message": "file uploaded"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        item = {
            "message": "profilePic must .jpg or .png"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)

@app.get("/user/profilePic", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_getProfilePic(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbUser = mydb.getDBUserData(decoded["Emailaddr"])
    if dbUser["ProfilePic"] is None:
        item = {
            "message": "there is no ProfilePic for User"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)
    else:
        path = "./imgs/" + dbUser["ProfilePic"]
        return FileResponse(path=path, filename=dbUser["ProfilePic"])
    return

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

@app.put("/user/update", dependencies=[Depends(JWTBearer())], tags=["user"], response_model=resMess)
async def user_update(Authorization: Optional[str] = Header(None), user: UserUpdate = Body(...)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    if mydb.updateUser(user, decoded["Emailaddr"]) == 1:
        item = {
            "message": "Update Success"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        item = {
            "message": "not managed err"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


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
