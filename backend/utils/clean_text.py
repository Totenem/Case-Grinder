import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, size=2000):
    return [text[i:i+size] for i in range(0, len(text), size)]