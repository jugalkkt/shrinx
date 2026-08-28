import email

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from app.models import User, clientSignupRequest
from app.core.hash import hash_password
from pymongo.errors import DuplicateKeyError
import asyncio
from app.core.template import templates


router = APIRouter()

@router.post("/signup")
async def signup(request: clientSignupRequest):
    # your logic here
    hashed_password = await asyncio.to_thread(hash_password, request.password)
    user = User(name=request.name,email=request.email,hashed_password=hashed_password)
    try:
        await user.insert()
    except DuplicateKeyError as e:
        return JSONResponse(status_code=409, content={"message": "email already registered!"})
    return RedirectResponse("/login", status_code=303)

@router.get("/signup", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(request, "signup.html")

@router.post("/signup/new")
async def signup_form(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # your logic here
    hashed_password = await asyncio.to_thread(hash_password, password)
    user = User(name=name,email=email,hashed_password=hashed_password)
    try:
        await user.insert()
    except DuplicateKeyError as e:
        return JSONResponse(status_code=409, content={"message": "email already registered!"})
    return RedirectResponse("/login", status_code=303)
    
    

