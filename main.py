# file that runs backend

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text  # Import text function
from db.database import *  # Ensure the import path is correct
from api.auth import auth
from api.rankings import rankings
from api.player import player
from db.database import database
from fastapi.middleware.cors import CORSMiddleware

# requiring database for application to connect
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# including routes for api
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(rankings.router, prefix="/rankings", tags=["rankings"])
app.include_router(player.router, prefix="/player", tags=["player"])

# allowing CORS -- do we need?
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to frontend url whenever we figure out what it is
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World - welcome to match point!"}
