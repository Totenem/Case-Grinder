import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#fcf8ff] flex flex-col items-center justify-center px-4 py-8 text-[#2f2041]">
      <div className="w-full max-w-3xl flex flex-col items-center gap-10">
        <header className="text-center">
          <h1 className="text-5xl font-semibold tracking-tight text-[#7c3aed]">
            Case Grinder
          </h1>
          <p className="mt-2 text-sm text-[#7f6a9a]">
            Analyze cases smarter and faster
          </p>
        </header>

        <div className="grid w-full grid-cols-1 gap-6 md:grid-cols-2">
          <Link
            href="/search"
            className="flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-[#7c3aed] bg-white p-10 text-center shadow-sm transition hover:bg-[#f5eeff] hover:shadow-md"
          >
            <span className="text-xl font-semibold text-[#7c3aed]">Search Cases</span>
            <span className="text-sm text-[#7f6a9a]">
              Find and generate digests from Philippine jurisprudence
            </span>
          </Link>

          <Link
            href="/upload"
            className="flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-[#d9c2ff] bg-white p-10 text-center shadow-sm transition hover:bg-[#f5eeff] hover:shadow-md"
          >
            <span className="text-xl font-semibold text-[#7c3aed]">Upload PDF</span>
            <span className="text-sm text-[#7f6a9a]">
              Generate a digest from your own PDF file
            </span>
          </Link>
        </div>
      </div>
    </main>
  );
}
