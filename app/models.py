from beanie import Document
from datetime import datetime


class User(Document):
    name: str
    email: str

class Link(Document):
    short_code: str
    destination: HttpUrl
    user: Link[User]
    created_at: datetime