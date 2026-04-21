from io import BytesIO
from pdfminer.high_level import extract_text

async def extract_text_from_pdf(file_bytes: bytes):
    return extract_text(BytesIO(file_bytes))