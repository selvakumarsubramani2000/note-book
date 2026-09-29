"""
query.py — Interactive CLI that answers questions using the indexed docs.

Make sure you've run 'python ingest.py' first.

Usage:
    python query.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# ─── Configuration ──────────────────────────────────────────────────────────
DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
TOP_K = 4

# ─── Load env ───────────────────────────────────────────────────────────────
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("❌ OPENAI_API_KEY not found. Copy .env.example to .env.")

if not Path(DB_PATH).exists():
    raise SystemExit(f"❌ Vector DB not found at '{DB_PATH}'. Run 'python ingest.py' first.")

# ─── Prompt Template ────────────────────────────────────────────────────────
# This is THE prompt sent to the LLM — the heart of RAG.
PROMPT = PromptTemplate.from_template(
    """You are a helpful assistant for AcmeCorp employees.
Use ONLY the context below to answer the question.
If the context doesn't contain the answer, say "I don't know based on the provided documents."
Be concise and cite relevant details.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
)


def build_qa_chain() -> RetrievalQA:
    """Load vector DB + LLM and wire up the RAG chain."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )


def format_sources(source_docs) -> str:
    """Pretty-print source chunks used for the answer."""
    lines = []
    for i, doc in enumerate(source_docs, 1):
        src = doc.metadata.get("source_name", "?")
        idx = doc.metadata.get("chunk_index", "?")
        preview = doc.page_content[:80].replace("\n", " ") + "..."
        lines.append(f"  [{i}] {src} (chunk {idx}) — \"{preview}\"")
    return "\n".join(lines)


def main() -> None:
    print("─" * 60)
    print("🧠 RAG Q&A Bot — ask me about AcmeCorp!")
    print("   Type 'exit' or 'quit' to stop. Type 'debug' to toggle source display.")
    print("─" * 60)

    qa = build_qa_chain()
    show_sources = True

    while True:
        try:
            question = input("\n❓ You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Bye!")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("👋 Bye!")
            break
        if question.lower() == "debug":
            show_sources = not show_sources
            print(f"🔧 Source display: {'ON' if show_sources else 'OFF'}")
            continue

        # ─── Run the RAG chain ──────────────────────────────────────────
        result = qa.invoke({"query": question})
        answer = result["result"]
        sources = result["source_documents"]

        print(f"\n🤖 Answer: {answer}")

        if show_sources and sources:
            print(f"\n📚 Sources ({len(sources)} chunks):")
            print(format_sources(sources))


if __name__ == "__main__":
    main()
