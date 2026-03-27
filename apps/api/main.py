from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from .routers import api as api_router
from .routers import pages as page_router
from .settings import get_settings

BASE_DIR = Path(__file__).resolve().parents[2]

app = FastAPI(title="CivicMap AI", description="Civic infrastructure intelligence platform")
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and templates
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Routers
app.include_router(api_router.router)
app.include_router(page_router.router)


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")
