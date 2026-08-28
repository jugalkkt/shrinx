from app.core import auth, shortcode
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.models import Link, User
from pymongo import AsyncMongoClient
from beanie import init_beanie
from datetime import datetime
from app.routes.links import router as links_router
from app.routes.auth import router as auth_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- this part runs once, at startup ----

    # Create Async PyMongo client
    client = AsyncMongoClient(settings.MONGODB_URI)
    #Init beanie with the Product document class
    await init_beanie(database=client["shrinx_db"], document_models=[Link, User]) 

    # make a placeholder till i implement proper auth
    # existing = await User.find_one(User.email == "akshay1@gmail.com")
    # if not existing:
    #     user = User(name="Akshay Varrier", email="akshay1@gmail.com")
    #     await user.insert()


    yield  # <-- the app runs here, handling requests, until shutdown

    # ---- this part runs once, at shutdown ----
    await client.close()
    print("shutting down")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(links_router)



