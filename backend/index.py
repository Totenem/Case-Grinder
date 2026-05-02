import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from dotenv import load_dotenv
from fastapi import UploadFile, File, HTTPException

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from utils.handler.limit_handler import rate_limit_handler

from service.generate_digest import generate_digest_with_pdf, generate_digest_with_pure_text
from utils.extract_text_from_pdf import extract_text_from_pdf
from utils.extract_text_from_docs import extract_text_from_docs
from utils.clean_text import clean_text, chunk_text
from service.scraper.ph_scraper import fetch_case_detail, search_cases
from service.scraper.models.data_model import CaseDetailRequest
import requests

load_dotenv()

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)

# Add middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_middleware(SlowAPIMiddleware)

cors_origins_env = os.getenv("CORS_ORIGINS", "")
origins = []

# Split the environment variable into raw parts
raw_origins = cors_origins_env.split(",")

for origin in raw_origins:
    # Remove surrounding whitespace
    cleaned_origin = origin.strip()
    
    # Only include non-empty values
    if cleaned_origin:
        origins.append(cleaned_origin)

if not origins:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Application": "Running"}

@app.post("/digest")
@limiter.limit("5/minute")
async def digest(file: UploadFile = File(...)):
    ALLOWED_PDF_MIME = {
        "application/pdf"
        }
    ALLOWED_DOCS_MIME = {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }

    try:
        filename = file.filename
        extension = os.path.splitext(filename)[1].lower()
        file_bytes = await file.read()

        if file.content_type in ALLOWED_PDF_MIME:
            if extension == ".pdf":
                text = await extract_text_from_pdf(file_bytes)
        elif file.content_type in ALLOWED_DOCS_MIME:
            if extension == ".docx":
                text = await extract_text_from_docs(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload a .pdf or .docx file.")

        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text)
        digest = await generate_digest_with_pdf(chunks)
        return {"digest": digest}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

@app.get("/search/{search}")
@limiter.limit("5/minute")
async def search_case(search: str, page: int = 1, rows: int = 10):
    results = search_cases(search, page=page, rows=rows)
    return {
        "data": results,
    }

@app.post("/search/results")
@limiter.limit("5/minute")
async def search_case_details(payload: CaseDetailRequest):

    #get the details
    details = await run_in_threadpool(fetch_case_detail, payload.source_url)

    #generate the digest
    detailed_text = await generate_digest_with_pure_text(details)

    return {
        "data": detailed_text,
    }

# @app.get("/get/models")
# async def get_models():

#     api_key = os.environ.get("GROQ_API_KEY")
#     url = "https://api.groq.com/openai/v1/models"

#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }

#     response = requests.get(url, headers=headers)

#     return response.json()