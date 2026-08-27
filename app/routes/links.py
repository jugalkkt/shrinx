from fastapi import APIRouter, status
from app.models import Link, User, clientRequest
from fastapi.responses import RedirectResponse, JSONResponse
from app.core.shortcode import generate_code
from datetime import datetime
# other imports you'll need

router = APIRouter()

@router.get("/{code}")
async def follow(code: str):
    # your logic here
    link1 = await Link.find_one(Link.short_code == code)
    if not link1:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND , content="404 not found!")
    return RedirectResponse(link1.destination, status_code=302)

@router.post("/links")
async def create_link(request: clientRequest):
    # your logic here
    short_code = generate_code(7)
    created_at = datetime.now()
    link1 = Link(short_code=short_code, destination=request.destination, user=user)
    return link1