from fastapi import APIRouter, status
from app.models import Link, User, clientRequest
from fastapi.responses import RedirectResponse, JSONResponse
from app.core.shortcode import generate_code
from datetime import date, datetime
from pymongo.errors import DuplicateKeyError
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
    # temporary placegolder user
    user = await User.find_one(User.email=="akshay1@gmail.com")
    max_retry = 5
    for i in range(max_retry):
        try:
            short_code = generate_code(7)
            created_at = datetime.now()
            link1 = Link(short_code=short_code, destination=request.destination, user=user, created_at=created_at)
            await link1.insert()
            return JSONResponse(
                status_code=201,
                content={"message": "Link created", "short_code":short_code}
            )
        except DuplicateKeyError as e:
            print(f'attempt {i} failed!')
    return JSONResponse(
        status_code=500,
        content={"message": "Server error"}
    )

    
    