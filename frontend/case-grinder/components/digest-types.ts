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
