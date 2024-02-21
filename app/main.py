from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth, vote 
from .config import settings

# from pydantic.v1 import BaseSettings
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     # path: int
#     database_username: str = "postgres"
#     secret_key: str = "sldfjlsfjs"

# settings = Settings()
# print(settings.DATABASE_USERNAME)

# models.Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# To run this in any website console you have to give CORS permission like below is giving google.com
# fetch('http://127.0.0.1:8000/').then(res => res.json()).then(console.log)
# origins = ["https://www.google.com"]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# while True:
#     try:
#         conn=psycopg2.connect(host="localhost", database="FastApi", user="postgres", password='Hathi8120', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed!")
#         print("Error: ", error)
#         time.sleep(2)

app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)       
app.include_router(vote.router)       

# Define a simple endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()
#     return {"data":posts}


