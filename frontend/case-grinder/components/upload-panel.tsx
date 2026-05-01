"use client";

import { ChangeEvent } from "react";
import { ClipLoader } from "react-spinners";

type UploadPanelProps = {
  selectedFile: File | null;
  loading: boolean;
  error: string;
  onFileChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onAnalyze: () => void;
};

export function UploadPanel({
  selectedFile,
  loading,
  error,
  onFileChange,
  onAnalyze,
}: UploadPanelProps) {
  return (
    <section className="rounded-xl border border-[#ead9ff] bg-white p-5 shadow-sm">
      <div className="grid gap-3 md:grid-cols-[1fr_auto]">
        <input
          type="file"
          accept="application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          disabled={loading}
          onChange={onFileChange}
          className="w-full cursor-pointer rounded-lg border border-[#d9c2ff] bg-white px-3 py-2 text-sm file:mr-4 file:rounded-md file:border-0 file:bg-[#f4edff] file:px-3 file:py-1.5 file:text-sm file:cursor-pointer"
        />
        <button
          type="button"
          onClick={onAnalyze}
          disabled={loading}
          className="rounded-lg bg-gradient-to-r from-[#db2777] to-[#7c3aed] px-5 py-2 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
        >
          {loading ? <ClipLoader className="white"></ClipLoader> : "Generate"}
        </button>
      </div>
      <p className="mt-2 text-xs text-[#6b5e7a]">
        {selectedFile ? `Successfully Uploaded: ${selectedFile.name}` : ""}
      </p>
      {error ? <p className="mt-2 text-sm text-[#be185d]">{error}</p> : null}
    </section>
  );
}     
