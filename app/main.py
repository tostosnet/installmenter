from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine
from . import models
from .config import Settings
from .routers import manager, post, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(manager.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API!!!"}

