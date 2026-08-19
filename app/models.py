from beanie import Document, Indexed
from datetime import datetime
from pydantic import HttpUrl



class User(Document):
    name: str
    email: str

class Link(Document):
    short_code: Indexed(str, unique = True)
    destination: HttpUrl
    user: Link[User]
    created_at: datetime