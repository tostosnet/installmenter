from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm.session import Session

from .. import models, schemas, utils, oauth2
from ..db import engine, get_db


router = APIRouter(
    prefix="/client",
    tags=["Clients"]
)

