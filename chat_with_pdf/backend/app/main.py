from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pathlib import Path
from app.api.routes import pdf_routes, chat_routes 
import traceback
from dotenv import load_dotenv  

# Load environment variables
load_dotenv()  
# Initializing app
app = FastAPI(title="Chat with PDF - Advanced RAG System")

# Configure paths
BASE_PATH = Path(__file__).resolve().parent
FRONTEND_PATH = BASE_PATH.parent.parent / "frontend"

# Mount static files
app.mount("/static", StaticFiles(directory=FRONTEND_PATH / "static"), name="static")

# Setup templates
templates = Jinja2Templates(directory=FRONTEND_PATH / "templates")

# global exception handler for debugging
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    print("=" * 60)
    print("UNHANDLED EXCEPTION OCCURRED:")
    print("=" * 60)
    print(f"Request URL: {request.url}")
    print(f"Request method: {request.method}")
    print(f"Exception type: {type(exc).__name__}")
    print(f"Exception message: {str(exc)}")
    print("Full traceback:")
    traceback.print_exc()
    print("=" * 60)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "detail": "Internal server error occurred"
        }
    )

# Include API routes
app.include_router(pdf_routes.router, prefix="/api/v1/pdf")
app.include_router(chat_routes.router, prefix="/api/v1/chat")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
