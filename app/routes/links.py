from fastapi import APIRouter, status, Request, Form
from app.models import Link, User, clientRequest
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from app.core.shortcode import generate_code, RESERVED_CODES
from datetime import date, datetime
from pymongo.errors import DuplicateKeyError
from app.core.template import templates
from pydantic import HttpUrl


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    user = await User.find_one(User.email=='akshay1@gmail.com')
    links = await Link.find(Link.user.id == user.id).to_list()
    return templates.TemplateResponse(request, "index.html",{"links":links})

# actual create_link
@router.post("/links/new")
async def create_link_form(destination: HttpUrl = Form(...)):
    # temporary placefolder user
    user = await User.find_one(User.email=="akshay1@gmail.com")
    max_retry = 5
    for i in range(max_retry):
        try:
            short_code = generate_code(7)
            if short_code in RESERVED_CODES:
                print(f'attempt {i} failed! - restricted keyword')
                continue
            created_at = datetime.now()
            link1 = Link(short_code=short_code, destination=destination, user=user, created_at=created_at)
            await link1.insert()
            return RedirectResponse("/", status_code=303)
        except DuplicateKeyError as e:
            print(f'attempt {i} failed! - duplicate key error')
    return JSONResponse(
        status_code=500,
        content={"message": "Server error"}
    )
    
# for json only - testing for programmer/contributor
@router.post("/links")
async def create_link(request: clientRequest):
    # your logic here
    # temporary placefolder user
    user = await User.find_one(User.email=="akshay1@gmail.com")
    max_retry = 5
    for i in range(max_retry):
        try:
            short_code = generate_code(7)
            if short_code in RESERVED_CODES:
                print(f'attempt {i} failed! - restricted keyword')
                continue

            created_at = datetime.now()
            link1 = Link(short_code=short_code, destination=request.destination, user=user, created_at=created_at)
            await link1.insert()
            return JSONResponse(
                status_code=201,
                content={"message": "Link created", "short_code":short_code}
            )
        except DuplicateKeyError as e:
            print(f'attempt {i} failed! - duplicate key error')
    return JSONResponse(
        status_code=500,
        content={"message": "Server error"}
    )

@router.get("/{code}")
async def follow(code: str):
    # your logic here
    link1 = await Link.find_one(Link.short_code == code)
    if not link1:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND , content="404 not found!")
    return RedirectResponse(link1.destination, status_code=302)

    
    