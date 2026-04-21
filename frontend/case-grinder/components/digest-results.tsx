import { DigestSection } from "./digest-types";

const FIELD_LABELS: Array<{ key: keyof DigestSection; label: string }> = [
  { key: "abstract", label: "Abstract" },
  { key: "facts", label: "Facts" },
  { key: "issues", label: "Issues" },
  { key: "ruling", label: "Ruling" },
  { key: "ratio", label: "Ratio" },
  { key: "summary", label: "Summary" },
];

type DigestResultsProps = {
  section: DigestSection;
};

export function DigestResults({ section }: DigestResultsProps) {
  return (
    <section className="rounded-xl border border-[#ead9ff] bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-4 border-b border-[#f0e8ff] pb-4">
        <div>
          <p className="text-xs uppercase tracking-wide text-[#7f6a9a]">Title</p>
          <h2 className="text-2xl font-semibold text-[#2f2041]">
            {section.title || "N/A"}
          </h2>
        </div>
        <div className="grid grid-cols-2 gap-6 text-sm">
          <div>
            <p className="text-xs uppercase tracking-wide text-[#7f6a9a]">Case</p>
            <p className="font-medium text-[#2f2041]">{section.case_number || "N/A"}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-[#7f6a9a]">
              Decision Date
            </p>
            <p className="font-medium text-[#2f2041]">{section.decision_date || "-"}</p>
          </div>
        </div>
      </div>

      <div className="mt-5 space-y-5">
        {FIELD_LABELS.map((field) => (
          <article key={field.key}>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-[#8d78a8]">
              {field.label}
            </h3>
            <p className="mt-1 whitespace-pre-wrap leading-7 text-[#322449]">
              {section[field.key] || "Not clearly stated in the provided text."}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
