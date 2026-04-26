"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ClipLoader } from "react-spinners";
import { DigestResults } from "@/components/digest-results";
import {
  DigestMode,
  DigestPayload,
  EMPTY_SECTION,
  SearchResult,
} from "@/components/digest-types";
import { ModeToggle } from "@/components/mode-toggle";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL?.trim() || "http://127.0.0.1:8000";

type ActivePanel = "results" | "digest";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [lastPage, setLastPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);

  const [digest, setDigest] = useState<DigestPayload | null>(null);
  const [digestError, setDigestError] = useState("");
  const [generatingUrl, setGeneratingUrl] = useState<string | null>(null);
  const [mode, setMode] = useState<DigestMode>("standard");
  const [activePanel, setActivePanel] = useState<ActivePanel>("results");

  const activeSection = useMemo(
    () => (digest ? digest[mode] : EMPTY_SECTION),
    [digest, mode]
  );

  const hasDigestContent = digest !== null || !!digestError || generatingUrl !== null;

  const fetchResults = async (page: number) => {
    const trimmed = query.trim();
    if (!trimmed) return;

    setSearchLoading(true);
    setSearchError("");
    setResults([]);
    setDigest(null);
    setDigestError("");
    setHasSearched(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/search/${encodeURIComponent(trimmed)}?page=${page}`
      );
      if (!response.ok) throw new Error("Search request failed.");
      const data = (await response.json()) as {
        data: {
          items: SearchResult[];
          total: number;
          current_page: number;
          last_page: number;
        };
      };
      setResults(data.data?.items ?? []);
      setCurrentPage(data.data?.current_page ?? page);
      setLastPage(data.data?.last_page ?? 1);
      setTotalResults(data.data?.total ?? 0);
    } catch (err) {
      setSearchError(err instanceof Error ? err.message : "Search failed.");
    } finally {
      setSearchLoading(false);
    }
  };

  const onSearch = async () => {
    setActivePanel("results");
    setCurrentPage(1);
    await fetchResults(1);
  };

  const onPageChange = (newPage: number) => {
    fetchResults(newPage);
  };

  const onGenerate = async (sourceUrl: string) => {
    setGeneratingUrl(sourceUrl);
    setDigestError("");
    setDigest(null);
    setActivePanel("digest");

    try {
      const response = await fetch(`${API_BASE_URL}/search/results`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_url: sourceUrl }),
      });
      if (!response.ok) throw new Error("Digest generation failed.");
      const data = (await response.json()) as { data: DigestPayload };
      if (!data.data?.standard || !data.data?.detailed) {
        throw new Error("Unexpected response format.");
      }
      setDigest(data.data);
    } catch (err) {
      setDigestError(
        err instanceof Error ? err.message : "Failed to generate digest."
      );
    } finally {
      setGeneratingUrl(null);
    }
  };

  const ResultsList = (
    <section className="rounded-xl border border-[#ead9ff] bg-white shadow-sm overflow-hidden flex flex-col h-full">
      <div className="border-b border-[#f0e8ff] px-5 py-3">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-[#7f6a9a]">
          {searchLoading
            ? "Searching..."
            : results.length > 0
            ? `Page ${currentPage} of ${lastPage} · ${totalResults} total`
            : "Search Results"}
        </h2>
      </div>
      <div className="divide-y divide-[#f0e8ff] overflow-y-auto max-h-[calc(100vh-360px)]">
        {searchLoading ? (
          <div className="flex justify-center py-10">
            <ClipLoader color="#7c3aed" />
          </div>
        ) : results.length === 0 ? (
          <p className="px-5 py-8 text-center text-sm text-[#7f6a9a]">
            No results found.
          </p>
        ) : (
          results.map((result, i) => (
            <div
              key={result.source_url ?? i}
              className="flex flex-col gap-1 px-5 py-4"
            >
              <p className="text-sm font-semibold leading-snug text-[#2f2041]">
                {result.title ?? "Untitled"}
              </p>
              {result.docket_number && (
                <p className="text-xs text-[#7f6a9a]">{result.docket_number}</p>
              )}
              {result.ponente && (
                <p className="text-xs text-[#7f6a9a]">
                  Ponente: {result.ponente}
                </p>
              )}
              <button
                type="button"
                onClick={() =>
                  result.source_url && onGenerate(result.source_url)
                }
                disabled={!result.source_url || generatingUrl !== null}
                className="mt-2 self-start rounded-md bg-gradient-to-r from-[#db2777] to-[#7c3aed] px-3 py-1.5 text-xs font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer min-w-[72px] flex items-center justify-center"
              >
                {generatingUrl === result.source_url ? (
                  <ClipLoader size={12} color="white" />
                ) : (
                  "Generate"
                )}
              </button>
            </div>
          ))
        )}
      </div>
      {!searchLoading && lastPage > 1 && (
        <div className="border-t border-[#f0e8ff] flex items-center justify-between px-5 py-3">
          <button
            type="button"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage <= 1}
            className="rounded-md border border-[#d9c2ff] px-3 py-1.5 text-xs font-medium text-[#7c3aed] transition hover:bg-[#f5eeff] disabled:cursor-not-allowed disabled:opacity-40"
          >
            ← Prev
          </button>
          <span className="text-xs text-[#7f6a9a]">
            {currentPage} / {lastPage}
          </span>
          <button
            type="button"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage >= lastPage}
            className="rounded-md border border-[#d9c2ff] px-3 py-1.5 text-xs font-medium text-[#7c3aed] transition hover:bg-[#f5eeff] disabled:cursor-not-allowed disabled:opacity-40"
          >
            Next →
          </button>
        </div>
      )}
    </section>
  );

  const DigestPanel = (
    <section className="flex flex-col gap-4">
      {generatingUrl ? (
        <div className="flex flex-1 items-center justify-center rounded-xl border border-[#ead9ff] bg-white py-20 shadow-sm">
          <ClipLoader color="#7c3aed" />
        </div>
      ) : digestError ? (
        <div className="rounded-xl border border-[#ead9ff] bg-white p-6 shadow-sm">
          <p className="text-sm text-[#be185d]">{digestError}</p>
        </div>
      ) : digest ? (
        <>
          <ModeToggle mode={mode} onChange={setMode} />
          <DigestResults section={activeSection} />
        </>
      ) : (
        <div className="flex flex-1 items-center justify-center rounded-xl border border-[#ead9ff] bg-white py-20 shadow-sm">
          <p className="text-sm text-[#7f6a9a]">
            Select a case and click Generate to create a digest.
          </p>
        </div>
      )}
    </section>
  );

  return (
    <main className="min-h-screen bg-[#fcf8ff] px-4 py-8 text-[#2f2041]">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6">
        <header className="flex items-center gap-4">
          <Link
            href="/"
            className="text-sm text-[#7f6a9a] hover:text-[#7c3aed] transition"
          >
            ← Back
          </Link>
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-[#7c3aed]">
              Search Cases
            </h1>
            <p className="text-sm text-[#7f6a9a]">
              Search Philippine jurisprudence
            </p>
          </div>
        </header>

        <section className="rounded-xl border border-[#ead9ff] bg-white p-4 shadow-sm">
          <div className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && onSearch()}
              placeholder="Search cases, docket numbers, keywords..."
              className="flex-1 rounded-lg border border-[#d9c2ff] bg-white px-3 py-2 text-sm outline-none focus:border-[#7c3aed]"
            />
            <button
              type="button"
              onClick={onSearch}
              disabled={searchLoading || !query.trim()}
              className="rounded-lg bg-gradient-to-r from-[#db2777] to-[#7c3aed] px-5 py-2 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
            >
              {searchLoading ? (
                <ClipLoader size={16} color="white" />
              ) : (
                "Search"
              )}
            </button>
          </div>
          {searchError && (
            <p className="mt-2 text-sm text-[#be185d]">{searchError}</p>
          )}
        </section>

        {hasSearched && (
          <>
            {/* Mobile: toggle bars + active panel */}
            <div className="flex flex-col gap-3 lg:hidden">
              {activePanel === "digest" && (
                <button
                  type="button"
                  onClick={() => setActivePanel("results")}
                  className="w-full flex items-center justify-between rounded-xl bg-gradient-to-r from-[#db2777] to-[#7c3aed] px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:opacity-90 cursor-pointer"
                >
                  <span>Search Results</span>
                  <span className="text-base">↑</span>
                </button>
              )}

              {activePanel === "results" && ResultsList}

              {activePanel === "results" && hasDigestContent && (
                <button
                  type="button"
                  onClick={() => setActivePanel("digest")}
                  className="w-full flex items-center justify-between rounded-xl bg-gradient-to-r from-[#db2777] to-[#7c3aed] px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:opacity-90 cursor-pointer"
                >
                  <span>Case Digest</span>
                  <span className="text-base">↓</span>
                </button>
              )}

              {activePanel === "digest" && DigestPanel}
            </div>

            {/* Desktop: side by side */}
            <div className="hidden lg:grid lg:grid-cols-[2fr_3fr] gap-6">
              {ResultsList}
              {DigestPanel}
            </div>
          </>
        )}
      </div>
    </main>
  );
}
