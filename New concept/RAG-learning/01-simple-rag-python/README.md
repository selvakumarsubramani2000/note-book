# 🟢 Project 1: Simple RAG Q&A Bot (Python)

Your first working RAG application. A CLI chatbot that answers questions about a fictional company using markdown docs.

---

## 🎯 What You'll Build

A two-step pipeline:

1. **`ingest.py`** → reads `sample-docs/`, chunks them, embeds them, saves to a local Chroma vector DB.
2. **`query.py`** → interactive CLI. You type a question, it retrieves relevant chunks, sends them to GPT-4o-mini, prints the answer + sources.

### Example Session

```
🧠 RAG Q&A Bot — ask me about AcmeCorp!
Type 'exit' to quit.

❓ You: What is the refund policy?

📑 Retrieved 3 chunks from: refund-policy.md, product-faq.md

🤖 Answer: AcmeCorp offers a 30-day money-back guarantee on all products.
Refunds are processed within 14 business days. Purchases over $500
require manager approval.

📚 Sources:
  - refund-policy.md (chunk 1)
  - refund-policy.md (chunk 2)
  - product-faq.md (chunk 3)
```

---

## 🛠️ Setup

### 1. Install Python 3.10+

Check with:
```powershell
python --version
```

### 2. Create virtual environment

```powershell
cd c:\Selva\Notes\HandsOn\rag-learning\01-simple-rag-python
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If `Activate.ps1` is blocked, run once as admin: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure OpenAI key

```powershell
copy .env.example .env
notepad .env
```

Paste your key:
```
OPENAI_API_KEY=sk-your-key-here
```

Get a key at: https://platform.openai.com/api-keys

---

## ▶️ Run It

### Step 1: Index the documents (run once)

```powershell
python ingest.py
```

**Expected output**:
```
📂 Loading documents from sample-docs/...
   ✓ refund-policy.md
   ✓ employee-handbook.md
   ✓ product-faq.md
✂️  Splitting into chunks... 12 chunks created
🔢 Generating embeddings...
🗄️  Saving to Chroma at ./chroma_db
✅ Done! Vector DB ready.
```

### Step 2: Start asking questions

```powershell
python query.py
```

Try these questions:
- *"What is the refund policy?"*
- *"How many vacation days do employees get?"*
- *"Is the Widget Pro waterproof?"*
- *"Who can approve refunds over $500?"*
- *"What color is the sky?"* ← should say "I don't know"

---

## 🧠 How It Works (Code Walkthrough)

### `ingest.py` — The Indexing Pipeline

```python
# 1. Load markdown files from sample-docs/
loader = DirectoryLoader("sample-docs/", glob="**/*.md")
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Embed and store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
```

### `query.py` — The Q&A Loop

```python
# 1. Load existing vector DB
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 2. Retrieve top-4 relevant chunks for the question
retriever = db.as_retriever(search_kwargs={"k": 4})

# 3. Build prompt & call LLM
chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
result = chain.invoke({"query": user_question})
```

---

## 🧪 Experiments to Try

1. **Change chunk size** in `ingest.py` to `200` or `1000` — see how answers change.
2. **Change `k`** in `query.py` from 4 to 1 or 10 — observe answer quality.
3. **Delete a doc** from `sample-docs/`, re-run `ingest.py`, ask a question about it.
4. **Add your own markdown file** to `sample-docs/` and re-index.
5. **Change the system prompt** in `query.py` to make the bot respond in pirate speak 🏴‍☠️

---

## ❓ Troubleshooting

| Error | Fix |
|-------|-----|
| `openai.AuthenticationError` | Bad API key — check `.env` |
| `No module named 'langchain_openai'` | Run `pip install -r requirements.txt` in active venv |
| `chromadb` build error | `python -m pip install --upgrade pip setuptools wheel` first |
| Answer says "I don't know" too often | Increase `k` or chunk overlap |

---

**Next**: [Project 2 — Chat with your Notes folder](../02-chat-with-notes/)
