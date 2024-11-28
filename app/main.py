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
#@ CORS
#~ Cross Origin Resource Sharing(CORS) allows you to make requests from a web browser on one domain to a server on a different domain
#~By default our API will only allow web browsers running on the same domain as our server to make requests to it.
#~ ebay.com ----CORS will🚫-----> API(google.com)
#~ ebay(ebay.com) ----CORS will✅----->API(ebay.com)
# To run this in any website console you have to give CORS permission like below is giving google.com
# fetch('http://127.0.0.1:8000/').then(res => res.json()).then(console.log)
# origins = ["https://www.google.com"]
#! If you want to set up a public API so that everyone can access it, then your origins would just be a wild(*)card. So this means every single domain or every single origin. But if your API is being configured for a specific web app, then you definitrly want to make sure that you provide a strict list of origins. So just whatever domain your web app is running on so that no one else can accidentally reach our application for some reason or another. It's just security best practices to really narrow down the scope of the origins that can actually access your API. For now i'm just going to leave this as set to everyone can access, when we actually go to deploy this it will little bit easier form a testing purpose.
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
    return {"message": "Bismallah, Let's Learn FastAPI!"}
    

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()
#     return {"data":posts}


