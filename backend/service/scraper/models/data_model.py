from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, Field

@dataclass(slots=True)
class LawphilCase:
    id: int | None
    docket_number: str | None
    decision_date: datetime | None
    title: str | None
    reference: str | None
    source_url: str | None
    pdf_available: bool
    pdf_path: str | None
    ponente: str | None
    subject: str | None


@dataclass(slots=True)
class LawphilCaseDetail:
    source_url: str
    docket_number: str | None
    title: str | None
    subject: str | None
    description: str | None
    body_text: str
    html_content: str


class CaseDetailRequest(BaseModel):
    source_url: str = Field(..., min_length=1)