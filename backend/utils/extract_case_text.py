from typing import Any
import json

def extract_case_text(input_value: Any) -> str:
    if input_value is None:
        return ""

    if isinstance(input_value, str):
        return input_value

    if isinstance(input_value, dict):
        parts = []
        for meta_key in ("title", "subject", "description"):
            val = input_value.get(meta_key)
            if isinstance(val, str) and val.strip():
                parts.append(val.strip())

        for body_key in ("body_text", "text", "content", "details"):
            val = input_value.get(body_key)
            if isinstance(val, str) and val.strip():
                parts.append(val.strip())
                break

        if parts:
            return "\n\n".join(parts)
        return json.dumps(input_value, ensure_ascii=False)

    # Supports dataclass/object payloads from scraper detail model.
    for attr in ("body_text", "text", "content", "description"):
        value = getattr(input_value, attr, None)
        if isinstance(value, str) and value.strip():
            return value

    return str(input_value)