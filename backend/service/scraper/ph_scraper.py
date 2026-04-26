from __future__ import annotations


import html
import re
from datetime import datetime
from typing import Any
from urllib.parse import urljoin
from service.scraper.models.data_model import LawphilCase, LawphilCaseDetail
# from models.data_model import LawphilCase, LawphilCaseDetail <---- FOR TESTING
import requests

API_URL = "https://lawphil.net/api/jurisprudence" 
CASE_ROOT_URL = "https://lawphil.net/judjuris/"
DEFAULT_TIMEOUT_SECONDS = 30


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = html.unescape(value)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n[ \t]+", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()
    return cleaned or None


def clean_citation(value: str | None) -> str | None:
    text = normalize_text(value)
    if not text:
        return None

    # Remove appended opinion labels from title display.
    marker_match = re.search(
        r"\b(Concurring Opinion|Dissenting Opinion|Separate Opinion)s?\b",
        text,
        flags=re.IGNORECASE,
    )
    if marker_match:
        text = text[: marker_match.start()].strip(" /-")
    return text or None


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    # API currently returns ISO-8601 with Z suffix.
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def build_case_url(relative_url: str | None) -> str | None:
    if not relative_url:
        return None
    return urljoin(CASE_ROOT_URL, relative_url.lstrip("/"))


def extract_first_url_query_search(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    value = html.unescape(match.group(1)).strip()
    return value or None


def clean_html_to_text(raw_html: str) -> str:
    content = re.sub(r"<!--.*?-->", " ", raw_html, flags=re.DOTALL)
    content = re.sub(
        r"<(script|style)[^>]*>.*?</\1>",
        " ",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    content = re.sub(r"<br\s*/?>", "\n", content, flags=re.IGNORECASE)
    content = re.sub(r"</p\s*>", "\n\n", content, flags=re.IGNORECASE)
    content = re.sub(r"<[^>]+>", " ", content)
    content = html.unescape(content)
    content = content.replace("\xa0", " ")
    content = re.sub(r"[ \t]+", " ", content)
    content = re.sub(r"\n[ \t]+", "\n", content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = content.strip()

    footer_marker = "The Lawphil Project - Arellano Law Foundation"
    footer_idx = content.find(footer_marker)
    if footer_idx != -1:
        content = content[:footer_idx].strip()
    return content


def fetch_case_detail(
    source_url: str,
    *,
    session: requests.Session | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> LawphilCaseDetail:
    client = session or requests
    response = client.get(source_url, timeout=timeout)
    response.raise_for_status()
    page_html = response.text

    title = extract_first_url_query_search(r"<title[^>]*>(.*?)</title>", page_html)

    # Get the subject descrip
    subject = extract_first_url_query_search(
        r'<meta[^>]+name=["\']subject["\'][^>]+content=["\'](.*?)["\']',
        page_html,
    )
    description = extract_first_url_query_search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        page_html,
    )

    body_html = extract_first_url_query_search(
        r"<blockquote[^>]*>(.*?)</blockquote>",
        page_html,
    )
    body_text = clean_html_to_text(body_html or page_html)

    docket_number = None
    docket_match = re.search(
        r"\b(?:G\.R\.|A\.M\.|A\.C\.|B\.M\.|JIB\s*FPI)\s*No\.?\s*[^,\n<]+",
        body_html or page_html,
        flags=re.IGNORECASE,
    )
    if docket_match:
        docket_number = normalize_text(docket_match.group(0))
    elif title:
        docket_number = normalize_text(title)

    return LawphilCaseDetail(
        source_url=source_url,
        docket_number=docket_number,
        title=normalize_text(title),
        subject=normalize_text(subject),
        description=normalize_text(description),
        body_text=body_text,
        html_content=page_html,
    )


def map_case(item: dict[str, Any]) -> LawphilCase:
    return LawphilCase(
        id=item.get("id"),
        docket_number=normalize_text(item.get("gr_number")),
        decision_date=parse_datetime(item.get("date")),
        title=clean_citation(item.get("citation")),
        reference=normalize_text(item.get("reference")),
        source_url=build_case_url(item.get("url")),
        pdf_available=bool(item.get("pdf_availability")),
        pdf_path=normalize_text(item.get("pdf_path")),
        ponente=normalize_text(item.get("ponente")),
        subject=normalize_text(item.get("subject")),
    )


def search_cases(
    search: str,
    page: int = 1,
    rows: int = 10,
    *,
    session: requests.Session | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    client = session or requests
    params = {"search": search, "page": page, "rows": rows}

    response = client.get(API_URL, params=params, timeout=timeout)
    response.raise_for_status()

    payload = response.json()
    raw_items = payload.get("data", [])
    mapped_items = [map_case(item) for item in raw_items]

    return {
        "current_page": payload.get("current_page"),
        "last_page": payload.get("last_page"),
        "per_page": payload.get("per_page"),
        "total": payload.get("total"),
        "items": mapped_items,
    }


def search_all_pages(
    search: str,
    *,
    rows: int = 100,
    session: requests.Session | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> list[LawphilCase]:
    current_page = 1
    results: list[LawphilCase] = []

    while True:
        page_data = search_cases(
            search=search,
            page=current_page,
            rows=rows,
            session=session,
            timeout=timeout,
        )
        results.extend(page_data["items"])

        last_page = page_data.get("last_page") or current_page
        if current_page >= last_page:
            break
        current_page += 1

    return results


if __name__ == "__main__":
    # Basic smoke test before wiring endpoints.
    test_query = "LUZ"
    result = search_cases(test_query, page=1, rows=10)

    print(
        f"query={test_query!r} total={result['total']} "
        f"page={result['current_page']}/{result['last_page']}"
    )
    for item in result["items"][:5]:
        print(f"- {item.docket_number} | {item.title} | {item.source_url}")

    if result["items"] and result["items"][0].source_url:
        detail = fetch_case_detail(result["items"][0].source_url)
        print(
            "\nDetail smoke test:",
            f"title={detail.title!r}",
            f"subject={detail.subject!r}",
            f"body_len={len(detail.body_text)}",
        )
