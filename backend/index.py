import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from dotenv import load_dotenv
from fastapi import UploadFile, File
from service.generate_digest import generate_digest_with_pdf, generate_digest_with_pure_text
from utils.extract_text_from_pdf import extract_text_from_pdf
from utils.clean_text import clean_text, chunk_text
from service.scraper.ph_scraper import fetch_case_detail, search_cases
from service.scraper.models.data_model import CaseDetailRequest

load_dotenv()

app = FastAPI()

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
async def digest (file: UploadFile = File(...)):
    #get file from upload
    file_bytes = await file.read()
    text = await extract_text_from_pdf(file_bytes)
    
    #clean text
    cleaned_text = clean_text(text)
    #chunk text
    chunks = chunk_text(cleaned_text)
    #generate digest
    digest = await generate_digest_with_pdf(chunks)
    return {"digest": digest}

@app.get("/search/{search}")
async def search_case(search: str, page: int = 1, rows: int = 10):
    results = search_cases(search, page=page, rows=rows)
    return {
        "data": results,
    }

@app.post("/search/results")
async def search_case_details(payload: CaseDetailRequest):

    #get the details
    details = await run_in_threadpool(fetch_case_detail, payload.source_url)

    #generate the digest
    detailed_text = await generate_digest_with_pure_text(details)

    return {
        "data": detailed_text,
    }