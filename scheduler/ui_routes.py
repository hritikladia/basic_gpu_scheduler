from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "ui"

@router.get("/", response_class=HTMLResponse)
async def dashboard():
    return (UI_DIR / "index.html").read_text()

@router.get("/job_view", response_class=HTMLResponse)
async def job_view():
    return (UI_DIR / "job.html").read_text()
