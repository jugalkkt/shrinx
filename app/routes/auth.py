import email
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from app.models import User, clientSignupRequest
from app.core.hash import hash_password
from pymongo.errors import DuplicateKeyError
import asyncio
from app.core.template import templates
from app.core.jwt import create_token
from app.core.hash import verify_password


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
async def signup_homepage(request: Request):
    return templates.TemplateResponse(request, "signup.html")

@router.get("/login", response_class=HTMLResponse)
async def login_homepage(request: Request):
    return templates.TemplateResponse(request, "login.html")

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

@router.post("/login/new")
async def login_form(email: str = Form(...), password: str = Form(...)):
    user = await User.find_one(User.email == email)
    if not user or not await asyncio.to_thread(verify_password, password, user.hashed_password):
        return JSONResponse(status_code=401, content={"message": "Incorrect email or password"})
    token = await asyncio.to_thread(create_token, str(user.id))
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("session", token, httponly=True, samesite="lax", max_age=7*24*60*60)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("session")
    return response

