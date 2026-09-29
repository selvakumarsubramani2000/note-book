# 🧠 RAG (Retrieval-Augmented Generation) — Hands-On Learning

Learn RAG by building real, working applications from scratch.

> **📖 Theory**: For concepts, see [../../topics/ai-ml/03-rag/guide-rag-comprehensive.md](../../topics/ai-ml/03-rag/guide-rag-comprehensive.md)
> **⚡ Quick Ref**: [../../topics/ai-ml/03-rag/quick-reference.md](../../topics/ai-ml/03-rag/quick-reference.md)

---

## 🎯 Learning Path

| # | Project | What You'll Build | Difficulty | Time |
|---|---------|-------------------|------------|------|
| 1 | [01-simple-rag-python](./01-simple-rag-python/) | A CLI chatbot that answers from sample company docs | 🟢 Beginner | 1–2 hours |
| 2 | [02-chat-with-notes](./02-chat-with-notes/) | Chat with your own `c:\Selva\Notes` folder | 🟡 Intermediate | 2–3 hours |

---

## 🧩 What You'll Learn

By the end of these projects, you'll have hands-on experience with:

- ✅ Loading documents (text, markdown, PDF)
- ✅ Chunking strategies
- ✅ Generating embeddings with OpenAI
- ✅ Storing & querying vector databases (Chroma)
- ✅ Building a full RAG pipeline with LangChain
- ✅ Prompt engineering for grounded answers
- ✅ Returning source citations
- ✅ Troubleshooting common RAG issues

---

## 🛠️ Prerequisites

### Software
- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- A code editor (VS Code recommended)
- Terminal / PowerShell

### API Keys (choose one path)

| Option | Cost | Setup |
|--------|------|-------|
| **OpenAI API** (recommended) | ~$1–2 total for all projects | [Get key](https://platform.openai.com/api-keys) |
| **Local (Ollama)** | Free | [Install Ollama](https://ollama.com/) + `ollama pull llama3.2` + `ollama pull nomic-embed-text` |

> 💡 **Tip**: Start with OpenAI for reliability. Switch to Ollama later if you want to go fully local/free.

---

## 📂 Folder Structure

```
HandsOn/rag-learning/
├── README.md                          ← You are here
├── 01-simple-rag-python/              ← Start here
│   ├── README.md
│   ├── requirements.txt
│   ├── ingest.py                      ← Loads & indexes docs
│   ├── query.py                       ← Interactive Q&A
│   ├── .env.example
│   └── sample-docs/                   ← Fake company docs to query
│       ├── refund-policy.md
│       ├── employee-handbook.md
│       └── product-faq.md
└── 02-chat-with-notes/                ← Capstone project
    ├── README.md
    ├── requirements.txt
    ├── ingest_notes.py                ← Indexes your Notes folder
    ├── chat.py                        ← Interactive chat CLI
    └── .env.example
```

---

## 🚀 Quick Start

```powershell
# 1. Clone or navigate to this folder
cd c:\Selva\Notes\HandsOn\rag-learning\01-simple-rag-python

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
copy .env.example .env
# Open .env and paste your OpenAI key

# 5. Index the sample documents
python ingest.py

# 6. Ask questions!
python query.py
```

---

## 💡 Learning Tips

1. **Don't skip Project 1** — Even if it seems simple, it teaches the full pipeline.
2. **Break things deliberately** — Change chunk sizes, ask weird questions, see what fails.
3. **Read the prompts** — Understanding what's sent to the LLM is 80% of RAG.
4. **Check retrieved chunks** — Both projects print what was retrieved so you can debug.
5. **Compare answers with/without RAG** — Ask the same question directly to ChatGPT vs. your RAG app.

---

## 🔍 Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Activate venv: `.\venv\Scripts\Activate.ps1` |
| `OpenAI API key not found` | Check `.env` file exists and has `OPENAI_API_KEY=sk-...` |
| `chromadb` install fails on Windows | Upgrade pip: `python -m pip install --upgrade pip` |
| Answers are poor | Check retrieved chunks — if they're irrelevant, improve chunking |
| Rate limit errors | Add `time.sleep(1)` between embedding calls or upgrade API tier |

---

## 🎓 Next Steps After These Projects

Once comfortable, try:
- 🔹 Add **re-ranking** using Cohere or a cross-encoder
- 🔹 Add **hybrid search** (vector + BM25)
- 🔹 Build a **Streamlit UI** instead of CLI
- 🔹 Try **Agentic RAG** with LangGraph
- 🔹 Replace OpenAI with **local Ollama** models (free, private)
- 🔹 Port it to **.NET + Semantic Kernel** (matches your main stack!)
- 🔹 Add **evaluation with RAGAS** (measure answer quality)

---

**Last Updated**: April 2026
