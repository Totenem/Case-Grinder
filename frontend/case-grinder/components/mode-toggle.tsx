"use client";

import { DigestMode } from "./digest-types";

type ModeToggleProps = {
  mode: DigestMode;
  onChange: (mode: DigestMode) => void;
};

export function ModeToggle({ mode, onChange }: ModeToggleProps) {
  return (
    <div className="mt-4 inline-flex rounded-md border border-[#e7dbff] bg-[#fcf9ff] p-1 text-sm">
      <button
        type="button"
        onClick={() => onChange("standard")}
        className={`rounded px-3 py-1.5 ${
          mode === "standard"
            ? "bg-gradient-to-r from-[#db2777] to-[#7c3aed] text-white"
            : "text-[#5f4d7f] hover:bg-[#f1e8ff]"
        }`}
      >
        Standard
      </button>
      <button
        type="button"
        onClick={() => onChange("detailed")}
        className={`rounded px-3 py-1.5 ${
          mode === "detailed"
            ? "bg-gradient-to-r from-[#db2777] to-[#7c3aed] text-white"
            : "text-[#5f4d7f] hover:bg-[#f1e8ff]"
        }`}
      >
        Detailed
      </button>
    </div>
  );
}
