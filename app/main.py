from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.models import Link, User
from pymongo import AsyncMongoClient
from beanie import init_beanie




@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- this part runs once, at startup ----

    # Create Async PyMongo client
    client = AsyncMongoClient(settings.MONGODB_URI)
    #Init beanie with the Product document class
    await init_beanie(database=client["shrinx_db"], document_models=[Link, User]) 

    yield  # <-- the app runs here, handling requests, until shutdown

    # ---- this part runs once, at shutdown ----
    print("shutting down")

app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello, world!"


