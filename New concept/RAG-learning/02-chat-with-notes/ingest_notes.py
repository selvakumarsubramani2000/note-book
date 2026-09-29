"""
ingest_notes.py — Indexes your personal Notes folder (all .md files) into
a local Chroma vector DB so you can chat with your knowledge base.

Usage:
    python ingest_notes.py                          # indexes c:\\Selva\\Notes
    python ingest_notes.py --path "D:\\my-notes"    # custom path
"""

import argparse
import os
import shutil
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# ─── Configuration ──────────────────────────────────────────────────────────
DEFAULT_NOTES_PATH = r"c:\Selva\Notes"
DB_PATH = "./notes_db"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "text-embedding-3-small"

# Directories to skip while walking
SKIP_DIRS = {
    "node_modules", "venv", ".venv", "__pycache__", ".git",
    "bin", "obj", "dist", "build", ".next", "chroma_db", "notes_db",
    "packages", ".vs", ".vscode", ".idea",
}

# ─── Load env ───────────────────────────────────────────────────────────────
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("❌ OPENAI_API_KEY not found. Copy .env.example to .env.")


def find_markdown_files(root: Path) -> list[Path]:
    """Walk the notes folder and return all .md files, skipping noisy dirs."""
    files: list[Path] = []
    for path in root.rglob("*.md"):
        # Skip if any parent dir is in SKIP_DIRS
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def load_documents(files: list[Path], root: Path) -> list[Document]:
    """Load .md files as LangChain Documents with rich metadata."""
    docs: list[Document] = []
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"   ⚠️  Skipping {fp} ({e})")
            continue

        if not text.strip():
            continue

        rel_path = str(fp.relative_to(root))
        modified = datetime.fromtimestamp(fp.stat().st_mtime).isoformat(timespec="seconds")

        docs.append(Document(
            page_content=text,
            metadata={
                "source": str(fp),
                "relative_path": rel_path,
                "file_name": fp.name,
                "modified": modified,
            },
        ))
    return docs


def main() -> None:
    parser = argparse.ArgumentParser(description="Index your notes into a vector DB.")
    parser.add_argument("--path", default=os.getenv("NOTES_PATH", DEFAULT_NOTES_PATH),
                        help="Root folder to index (default: c:\\Selva\\Notes)")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        raise SystemExit(f"❌ Folder not found: {root}")

    print("🧠 Notes Ingestion Pipeline\n" + "─" * 55)
    print(f"📂 Indexing: {root}")

    # 1. FIND + LOAD ────────────────────────────────────────────────────────
    files = find_markdown_files(root)
    if not files:
        raise SystemExit("❌ No markdown files found.")
    print(f"   ✓ Found {len(files)} .md files")

    docs = load_documents(files, root)
    print(f"   ✓ Loaded {len(docs)} non-empty documents")

    # 2. CHUNK ──────────────────────────────────────────────────────────────
    print(f"\n✂️  Splitting (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # Markdown-aware separators: prefer splitting at headings/blank lines
        separators=["\n# ", "\n## ", "\n### ", "\n#### ", "\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"   ✓ Created {len(chunks)} chunks")

    # Add a chunk index per file for easier debugging
    counters: dict[str, int] = {}
    for c in chunks:
        key = c.metadata["relative_path"]
        counters[key] = counters.get(key, 0) + 1
        c.metadata["chunk_index"] = counters[key]

    # 3. EMBED + STORE ──────────────────────────────────────────────────────
    print(f"\n🔢 Generating embeddings with '{EMBEDDING_MODEL}'...")
    print("   (this may take 30–90 seconds depending on size)")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    if Path(DB_PATH).exists():
        print(f"🧹 Removing existing DB at {DB_PATH}")
        shutil.rmtree(DB_PATH)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH,
    )
    print(f"🗄️  Saved to '{DB_PATH}'")
    print("\n✅ Done! Run 'python chat.py' to start chatting with your notes.\n")


if __name__ == "__main__":
    main()
