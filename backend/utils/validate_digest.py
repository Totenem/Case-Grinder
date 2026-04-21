TOP_LEVEL_KEYS = ["standard", "detailed"]
SECTION_KEYS = [
    "title",
    "case_number",
    "decision_date",
    "abstract",
    "facts",
    "issues",
    "ruling",
    "ratio",
    "summary",
]


def validate_digest_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Model response is not a JSON object.")

    if list(payload.keys()) != TOP_LEVEL_KEYS:
        raise ValueError(
            f"Invalid digest schema. Expected keys in order: {TOP_LEVEL_KEYS}."
        )

    for section in TOP_LEVEL_KEYS:
        section_payload = payload[section]
        if not isinstance(section_payload, dict):
            raise ValueError(f"Invalid type for '{section}'. Expected object.")

        if list(section_payload.keys()) != SECTION_KEYS:
            raise ValueError(
                f"Invalid '{section}' schema. Expected keys in order: {SECTION_KEYS}."
            )

        for key in SECTION_KEYS:
            if not isinstance(section_payload[key], str):
                raise ValueError(
                    f"Invalid type for '{section}.{key}'. Expected string."
                )

    return payload
