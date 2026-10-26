# ── Read .env FIRST — before any other imports touch os.environ ──────────────
import os, pathlib

def _load_env_file():
    """Parse .env file and inject variables into os.environ."""
    env_path = pathlib.Path(__file__).parent / ".env"
    if not env_path.is_file():
        return
    with open(env_path, "r", encoding="utf-8-sig") as f:   # utf-8-sig strips BOM
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key   = key.strip()
            value = value.strip().strip("'\"")
            if key and value and key not in os.environ:
                os.environ[key] = value

_load_env_file()   # runs before ANY other module import
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.agent import analyze_dataset

import traceback

app = FastAPI(title="AI Data Analysis Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure required directories exist before mounting
UPLOAD_FOLDER = "uploads"
CHARTS_FOLDER = os.path.join("static", "charts")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHARTS_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ALLOWED_EXTENSIONS = {".csv", ".xlsx"}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(
        file: UploadFile = File(...),
        query: str = Form(...)
):
    # ── Validate extension ────────────────────────────────────────────────
    _, ext = os.path.splitext(file.filename or "")
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel (.xlsx) files are supported."
        )

    # ── Save uploaded file ────────────────────────────────────────────────
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # ── Run analysis ──────────────────────────────────────────────────────
    try:
        result = analyze_dataset(file_path, query)
    except Exception as e:
        print(f"[ERROR] Analysis failed:\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=200,
            content={
                "answer": f"⚠️ Analysis failed: {str(e)}",
                "has_chart": False,
                "chart_url": None
            }
        )

    # ── Detect generated chart ────────────────────────────────────────────
    chart_filename = "temp_chart.png"
    chart_path = os.path.join(CHARTS_FOLDER, chart_filename)
    has_chart = os.path.exists(chart_path)

    return {
        "answer": result,
        "has_chart": has_chart,
        "chart_url": f"/static/charts/{chart_filename}" if has_chart else None
    }