import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import UploadFile, File
from service.generate_digest import generate_digest
from utils.extract_text_from_pdf import extract_text_from_pdf
from utils.clean_text import clean_text, chunk_text

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
    digest = await generate_digest(chunks)
    return {"digest": digest}
