import json
import os

from groq import Groq
from utils.validate_digest import validate_digest_payload


async def generate_digest(chunks):
    case_text = "\n\n".join(chunks) if isinstance(chunks, list) else str(chunks)
    groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert legal analyst AI for case-law summarization.\n\n"
                    "You must output exactly one valid JSON object.\n"
                    "Do not output markdown.\n"
                    "Do not output code fences.\n"
                    "Do not output any text before or after JSON.\n"
                    "Do not include any keys other than the required keys.\n\n"
                    "Required JSON schema (exact keys, exact order):\n"
                    '{\n  "standard": {\n    "title": "",\n    "case_number": "",\n    "decision_date": "",\n    "abstract": "",\n    "facts": "",\n    "issues": "",\n    "ruling": "",\n    "ratio": "",\n    "summary": ""\n  },\n  "detailed": {\n    "title": "",\n    "case_number": "",\n    "decision_date": "",\n    "abstract": "",\n    "facts": "",\n    "issues": "",\n    "ruling": "",\n    "ratio": "",\n    "summary": ""\n  }\n}\n\n'
                    "Instructions:\n"
                    "- Analyze only the provided case text.\n"
                    '- If information is missing/unclear, write: "Not clearly stated in the provided text."\n'
                    '- Include "title" (case name) and "case_number" if available.\n'
                    '- "decision_date" may be an empty string if unavailable.\n'
                    '- "abstract" should be a short overview of the full case.\n'
                    '- For "standard": keep each field concise and practical for quick review.\n'
                    '- For "detailed": provide richer legal context, finer distinctions, and fuller reasoning.\n'
                    "- Use plain text in string values (no bullets, no numbering).\n"
                    "- Ensure JSON is parseable (double quotes, escaped characters, no trailing commas).\n\n"
                    "Return only the JSON object."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Create a legal case digest from the following case text.\n\n"
                    "Return format requirements:\n"
                    "- Output ONLY one valid JSON object\n"
                    "- Top-level keys must be exactly: standard, detailed\n"
                    "- Under both standard and detailed, use exactly these keys in this order:\n"
                    "  title, case_number, decision_date, abstract, facts, issues, ruling, ratio, summary\n"
                    '- "decision_date" can be an empty string if not stated\n'
                    "- No extra keys\n"
                    "- No markdown or explanations\n\n"
                    f"Case text:\n{case_text}"
                ),
            },
        ]
    )
    raw_content = (response.choices[0].message.content or "").strip()

    #validate raw content is a valid JSON object
    if not (raw_content.startswith("{") and raw_content.endswith("}")):
        raise ValueError("Model response is not raw JSON.")

    #load raw content into a dictionary
    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError("Model returned invalid JSON.") from exc

    #validate payload is a valid digest payload
    return validate_digest_payload(payload)