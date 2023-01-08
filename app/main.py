from fastapi import FastAPI, Path, Response, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.params import Body

from pydantic import BaseModel
from datetime import datetime, date

from app.news_extraction import *
from app.analysts_ratings import *

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import models
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

from .routers import posts

models.Base.metadata.create_all(bind=engine)

today = date.today()
start_date = today.today()
start_date = start_date.strftime("%m-%d-%Y")

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)

@app.get('/')
def home():
    return {"Homepage":"WELCOME TO ALTAPI!!"}