from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, engine, get_db
from routers import address

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(address.router)
