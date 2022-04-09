from fastapi import FastAPI
from app.db import DB


app = FastAPI()
mydb = DB()
