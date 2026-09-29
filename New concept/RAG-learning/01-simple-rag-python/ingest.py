"""
ingest.py — Loads markdown documents, chunks them, embeds them, and stores
in a local Chroma vector database.

Run once (or whenever docs change):
    python ingest.py
"""

import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# ─── Configuration ──────────────────────────────────────────────────────────
DOCS_PATH = "sample-docs"
DB_PATH = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "text-embedding-3-small"

# ─── Load env (OPENAI_API_KEY) ──────────────────────────────────────────────
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("❌ OPENAI_API_KEY not found. Copy .env.example to .env and fill in your key.")


def main() -> None:
    print("🧠 RAG Ingestion Pipeline\n" + "─" * 50)

    # 1. LOAD ───────────────────────────────────────────────────────────────
    print(f"📂 Loading documents from '{DOCS_PATH}/'...")
    if not Path(DOCS_PATH).exists():
        raise SystemExit(f"❌ Folder '{DOCS_PATH}' not found.")

    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=False,
    )
    docs = loader.load()

    if not docs:
        raise SystemExit(f"❌ No .md files found in '{DOCS_PATH}/'.")

    for doc in docs:
        source = Path(doc.metadata.get("source", "?")).name
        print(f"   ✓ {source} ({len(doc.page_content)} chars)")

    # 2. CHUNK ──────────────────────────────────────────────────────────────
    print(f"\n✂️  Splitting documents (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"   ✓ Created {len(chunks)} chunks")

    # Add a chunk index per source for easier debugging
    source_counters: dict[str, int] = {}
    for chunk in chunks:
        src = Path(chunk.metadata.get("source", "?")).name
        source_counters[src] = source_counters.get(src, 0) + 1
        chunk.metadata["source_name"] = src
        chunk.metadata["chunk_index"] = source_counters[src]

    # 3. EMBED + STORE ──────────────────────────────────────────────────────
    print(f"\n🔢 Generating embeddings with '{EMBEDDING_MODEL}'...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # Clean old DB to avoid duplicate docs on re-runs
    if Path(DB_PATH).exists():
        print(f"🧹 Removing existing DB at {DB_PATH}")
        shutil.rmtree(DB_PATH)

    print(f"🗄️  Saving to Chroma at '{DB_PATH}'...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH,
    )

    print("\n✅ Done! Vector DB ready.")
    print(f"   Run 'python query.py' to start asking questions.\n")


if __name__ == "__main__":
    main()
