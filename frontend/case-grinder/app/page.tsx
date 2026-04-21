"use client";

import { ChangeEvent, useMemo, useState } from "react";
import { DigestResults } from "@/components/digest-results";
import { DigestMode, DigestPayload, EMPTY_SECTION } from "@/components/digest-types";
import { ModeToggle } from "@/components/mode-toggle";
import { UploadPanel } from "@/components/upload-panel";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL?.trim() || "http://127.0.0.1:8000";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [mode, setMode] = useState<DigestMode>("standard");
  const [digest, setDigest] = useState<DigestPayload | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const activeSection = useMemo(
    () => (digest ? digest[mode] : EMPTY_SECTION),
    [digest, mode]
  );

  const onFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setSelectedFile(file);
    setError("");
  };

  const onAnalyze = async () => {
    if (!selectedFile) {
      setError("Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/digest`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Digest request failed.");
      }

      const data = (await response.json()) as { digest?: DigestPayload };

      if (!data.digest?.standard || !data.digest?.detailed) {
        throw new Error("Unexpected response format.");
      }

      setDigest(data.digest);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "Failed to generate digest.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#fcf8ff] px-4 py-8 text-[#2f2041]">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-6">
        <header className="text-center">
          <h1 className="text-5xl font-semibold tracking-tight text-[#7c3aed]">
            Case Grinder
          </h1>
          <p className="mt-2 text-sm text-[#7f6a9a]">
            Analyze cases smarter and faster
          </p>
        </header>

        <UploadPanel
          selectedFile={selectedFile}
          loading={loading}
          error={error}
          onFileChange={onFileChange}
          onAnalyze={onAnalyze}
        />

        {digest ? (
          <>
            <ModeToggle mode={mode} onChange={setMode} />
            <DigestResults section={activeSection} />
          </>
        ) : null}
      </div>
    </main>
  );
}
