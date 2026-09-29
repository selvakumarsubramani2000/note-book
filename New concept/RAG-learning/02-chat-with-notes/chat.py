"""
chat.py — Multi-turn chat CLI over your indexed Notes folder.

Uses conversation memory so follow-up questions work naturally:
    "What is RAG?"
    "What are its types?"      ← understood as "types of RAG"

Make sure 'python ingest_notes.py' was run first.

Usage:
    python chat.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# ─── Configuration ──────────────────────────────────────────────────────────
DB_PATH = "./notes_db"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
TOP_K = 5

# ─── Load env ───────────────────────────────────────────────────────────────
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("❌ OPENAI_API_KEY not found. Copy .env.example to .env.")

if not Path(DB_PATH).exists():
    raise SystemExit(f"❌ Vector DB not found at '{DB_PATH}'. Run 'python ingest_notes.py' first.")

# ─── Prompts ────────────────────────────────────────────────────────────────
# Rewrites a follow-up question into a standalone question using chat history.
CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Given a chat history and the latest user question which might reference context "
     "in the chat history, reformulate the question into a standalone question that can "
     "be understood without the chat history. Do NOT answer — just reformulate if needed."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Answers the question using retrieved context.
ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a personal knowledge assistant answering questions from the user's own "
     "learning notes. Use ONLY the context below. If the context doesn't contain the "
     "answer, say 'I don't see that in your notes.' Be concise, use bullet points for "
     "lists, and reference specific files/topics when helpful.\n\nCONTEXT:\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


def build_chain():
    """Wire up history-aware retriever + answer chain."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)

    history_aware = create_history_aware_retriever(llm, retriever, CONTEXTUALIZE_PROMPT)
    answer_chain = create_stuff_documents_chain(llm, ANSWER_PROMPT)
    return create_retrieval_chain(history_aware, answer_chain)


def format_sources(docs) -> str:
    """Show which notes were used to answer."""
    seen = set()
    lines = []
    for i, doc in enumerate(docs, 1):
        rel = doc.metadata.get("relative_path", "?")
        chunk_idx = doc.metadata.get("chunk_index", "?")
        key = (rel, chunk_idx)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"  [{i}] {rel}  (chunk {chunk_idx})")
        if len(lines) >= 5:
            break
    return "\n".join(lines) if lines else "  (no sources)"


def count_indexed() -> int:
    """Return approx. number of chunks in the DB."""
    try:
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        return db._collection.count()
    except Exception:
        return -1


def main() -> None:
    print("─" * 60)
    print("🧠 Chat with your Notes")
    n = count_indexed()
    if n > 0:
        print(f"   Indexed chunks: {n}")
    print("   Type 'exit' to quit, 'clear' to reset chat history.")
    print("─" * 60)

    chain = build_chain()
    chat_history: list = []

    while True:
        try:
            q = input("\n❓ You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Bye!")
            break

        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            print("👋 Bye!")
            break
        if q.lower() == "clear":
            chat_history = []
            print("🧹 Chat history cleared.")
            continue

        result = chain.invoke({"input": q, "chat_history": chat_history})

        answer = result["answer"]
        sources = result.get("context", [])

        print(f"\n🤖 Answer:\n{answer}")
        print(f"\n📚 Sources:\n{format_sources(sources)}")

        # Update history for next turn (keep last 6 turns to stay under token limits)
        chat_history.append(HumanMessage(content=q))
        chat_history.append(AIMessage(content=answer))
        chat_history = chat_history[-12:]


if __name__ == "__main__":
    main()
