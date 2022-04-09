from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import DB


User = []

app = FastAPI()
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


@app.get("/", tags=["root"])
async def read_root() -> dict:
    item = {"message": "WORKING !!!"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)
