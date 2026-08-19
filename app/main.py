from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
from pydantic import HttpUrl

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- this part runs once, at startup ----

    # Create Async PyMongo client
    client = AsyncMongoClient("mongodb://user:pass@host:27017")
    #Init beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=[Product])

    yield  # <-- the app runs here, handling requests, until shutdown

    # ---- this part runs once, at shutdown ----
    print("shutting down")

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello, world!"


