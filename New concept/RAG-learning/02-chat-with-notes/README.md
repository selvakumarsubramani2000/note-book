# 🟡 Project 2: Chat With Your Notes (Capstone)

Turn your `c:\Selva\Notes\` folder into a searchable AI assistant. Ask questions about what you've learned — JWT, SQL, backend architecture, RAG, etc. — and get grounded answers with source citations.

> ✅ Finish [Project 1](../01-simple-rag-python/) first. This one builds on the same concepts.

---

## 🎯 What You'll Build

A personal "second brain" that:

- 📂 Loads all `.md` files from `c:\Selva\Notes\`
- ✂️ Chunks them intelligently (respects markdown structure)
- 🔢 Embeds them with OpenAI
- 🗄️ Stores them in a local Chroma vector DB
- 💬 Answers your questions via a chat CLI with source citations

### Example Session

```
🧠 Chat with your Notes folder!
Indexed 47 files, 312 chunks from c:\Selva\Notes

❓ You: What did I learn about JWT authentication?

🤖 Answer: From your notes on JWT Authentication (Day-04):
JWT (JSON Web Token) is a stateless auth mechanism used in the
vendor-directory-app. It consists of 3 parts: header, payload, signature...

📚 Sources:
  [1] HandsOn\request-pipeline-di\Day-04-JWT-Authentication-Role-Authorization.md
  [2] topics\authentication-authorization\README.md

❓ You: What vector databases did I read about in the RAG guide?

🤖 Answer: Your RAG guide lists these vector databases:
- Pinecone (managed, production-scale)
- Chroma (lightweight, for prototyping)
- pgvector (use existing PostgreSQL)
- Qdrant (high performance, Rust-based)
...
```

---

## 🛠️ Setup

```powershell
cd c:\Selva\Notes\HandsOn\rag-learning\02-chat-with-notes
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env   # add your OPENAI_API_KEY
```

---

## ▶️ Run It

### Step 1: Index your Notes folder

```powershell
python ingest_notes.py
```

By default it indexes `c:\Selva\Notes\`. To index a different folder:
```powershell
python ingest_notes.py --path "D:\my-other-notes"
```

**Expected output**:
```
🧠 Indexing c:\Selva\Notes
📂 Found 47 .md files
✂️  Split into 312 chunks
🔢 Embedding... (this may take 30–60 seconds)
🗄️  Saved to ./notes_db
✅ Done!
```

### Step 2: Chat with your notes

```powershell
python chat.py
```

Try questions like:
- *"What did I learn about SQL JOINs?"*
- *"Summarize my backend architecture notes"*
- *"What tech stack am I using for vendor-directory-app?"*
- *"What are the types of RAG I studied?"*
- *"What's the difference between middleware and filters in .NET?"*

---

## 🧠 How It Differs From Project 1

| Feature | Project 1 | Project 2 |
|---------|-----------|-----------|
| Document source | Fixed `sample-docs/` | Configurable, defaults to your Notes |
| Chunking | Basic recursive | Markdown-aware (preserves headings) |
| Chat style | Single-turn Q&A | Multi-turn with **conversation memory** |
| Metadata | File name only | File path, heading, modified date |
| Source display | Short preview | Full relative path + line preview |

---

## 🧪 Cool Experiments

1. **Compare models**: Change `CHAT_MODEL` to `gpt-4o` vs `gpt-4o-mini` — is the quality worth the cost?
2. **Chunk size test**: Try chunk sizes 200, 500, 1000 — observe answer quality and speed.
3. **Add PDFs**: Drop a PDF into your Notes folder, modify `ingest_notes.py` to support it (hint: `PyPDFLoader`).
4. **Add re-indexing trigger**: Only re-embed files that changed since the last run.
5. **Web UI**: Replace the CLI with Streamlit (`pip install streamlit`, ~20 lines of code).

---

## 🎁 Bonus Challenge

Add this feature yourself: after every answer, ask the user "Was this helpful? (y/n)" and log the result to a CSV. That's the first step toward **RAG evaluation & continuous improvement**.

---

## ❓ Troubleshooting

| Issue | Fix |
|-------|-----|
| `FileNotFoundError: c:\Selva\Notes` | Use `--path` arg or edit `DEFAULT_NOTES_PATH` in `ingest_notes.py` |
| Embedding costs too much | Use `text-embedding-3-small` (already default) — ~$0.02 for all notes |
| Answers cite wrong files | Increase `TOP_K` or lower `CHUNK_SIZE` for better granularity |
| Rate limit on OpenAI | Reduce parallelism or wait 60 sec; free tier = 3 req/min |

---

## 💡 What's Next?

Now you have a **real, personal, working RAG app**. To level up:

1. **Port this to .NET + Semantic Kernel** (your main stack)
2. **Add a React frontend** calling a FastAPI backend with this logic
3. **Add Agentic RAG** — let the LLM ask follow-up questions
4. **Add evaluation** with RAGAS — measure your system's quality
5. **Deploy it** — host on Azure with your existing Azure AI Search skills

---

**Last Updated**: April 2026
