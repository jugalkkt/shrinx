from fastapi import APIRouter, status
from app.models import Link, User
from fastapi.responses import RedirectResponse, JSONResponse

# other imports you'll need

router = APIRouter()

@router.get("/{code}")
async def follow(code: str):
    # your logic here
    link1 = await Link.find_one(Link.short_code == code)
    if not link1:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND , content="404 not found!")
    return RedirectResponse(link1.destination, status_code=302)
