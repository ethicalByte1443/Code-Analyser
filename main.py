from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()


app = FastAPI()

# Static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates_dir = Path(__file__).parent / "views"
templates = Jinja2Templates(directory=templates_dir)

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.ejs", {"request": request})


def analyze_js(content: str):
    # Analysis logic for JavaScript files
    score = 0
    breakdown = {
        "naming": 8,
        "modularity": 15,
        "comments": 10,
        "formatting": 12,
        "reusability": 10,
        "best_practices": 15,
    }
    recommendations = [
        "Use consistent camelCase for function names.",
        "Refactor large functions into smaller, reusable components.",
        "Add comments to explain complex logic."
    ]
    score = sum(breakdown.values())
    return {
        "overall_score": score,
        "breakdown": breakdown,
        "recommendations": recommendations
    }

def analyze_py(content: str):
    # Analysis logic for Python files
    score = 0
    breakdown = {
        "naming": 9,
        "modularity": 17,
        "comments": 15,
        "formatting": 14,
        "reusability": 13,
        "best_practices": 16,
    }
    recommendations = [
        "Use snake_case for function and variable names.",
        "Add docstrings to all functions and classes.",
        "Avoid using single-letter variable names."
    ]
    score = sum(breakdown.values())
    return {
        "overall_score": score,
        "breakdown": breakdown,
        "recommendations": recommendations
    }

@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)):
    # Read the uploaded file content
    content = (await file.read()).decode("utf-8")
    file_extension = file.filename.split(".")[-1]

    if file_extension in ["js", "jsx"]:
        # Analyze JavaScript files
        analysis_result = analyze_js(content)
    elif file_extension == "py":
        # Analyze Python files
        analysis_result = analyze_py(content)
    else:
        # Unsupported file type
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

    return JSONResponse(content=analysis_result)
