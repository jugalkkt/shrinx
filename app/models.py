from enum import unique

from beanie import Document, Indexed, Link
from datetime import datetime
from pydantic import HttpUrl, BaseModel

class User(Document):
    name: str
    email: Indexed(str, unique = True)

class Link(Document):
    short_code: Indexed(str, unique = True)
    destination: HttpUrl
    user: Link[User]
    created_at: datetime

# TODO: private/internal IP addresses not yet rejected — see part 12 item 4
class clientRequest(BaseModel):
    destination: HttpUrl 