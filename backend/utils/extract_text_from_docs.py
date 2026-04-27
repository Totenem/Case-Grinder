from io import BytesIO
from docx import Document

async def extract_text_from_docs(file_bytes: bytes) -> str:
    doc = Document(BytesIO(file_bytes))
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
