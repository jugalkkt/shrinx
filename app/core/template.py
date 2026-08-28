from fastapi.templating import Jinja2Templates
import pathlib

templates = Jinja2Templates(directory=pathlib.Path(__file__).resolve().parent.parent.parent / "templates")

