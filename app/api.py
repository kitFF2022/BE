from fastapi import FastAPI, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import DB
from app.models.user import User, UserSignIn
from app.models.exModels import resMess, resSignin
from app.auth.auth_handler import signJWT

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
    if mydb.signinUser(user):
        return signJWT(user.Emailaddr)
    else:
        item = {
            "error": "Signin Failed"
        }
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post("/user/signup", tags=["user"], response_model=resMess)
async def user_signup(user: User = Body(...)):
    if mydb.signupUser(user):
        item = {
            "message": "signup success"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        item = {
            "message": "signup failed - > might be duplicated Emailaddr"
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=item)

    # if mydb.signupUser(user):
    #    return JSONResponse(status_code=status.HTTP_200_OK)
    # else:
    #    return JSONResponse(status_code=status.HTTP_401)


@app.get("/TEST/DB/DROPTABLE", tags=["TEST"], response_model=resMess)
async def test_DropTable():
    if mydb.WarnTestDelAllTableData():
        item = {
            "message": "All tables DROPED and CREATED"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        item = {
            "message": "internal server error"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)
