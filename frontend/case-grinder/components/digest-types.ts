export type SearchResult = {
  id: number | null;
  docket_number: string | null;
  decision_date: string | null;
  title: string | null;
  reference: string | null;
  source_url: string | null;
  pdf_available: boolean;
  pdf_path: string | null;
  ponente: string | null;
  subject: string | null;
};

export type DigestSection = {
  title: string;
  case_number: string;
  decision_date: string;
  abstract: string;
  facts: string;
  issues: string;
  ruling: string;
  ratio: string;
  summary: string;
};

export type DigestPayload = {
  standard: DigestSection;
  detailed: DigestSection;
};

export type DigestMode = "standard" | "detailed";

export const EMPTY_SECTION: DigestSection = {
  title: "",
  case_number: "",
  decision_date: "",
  abstract: "",
  facts: "",
  issues: "",
  ruling: "",
  ratio: "",
  summary: "",
};
