---
title: SHL Backend
emoji: 🏆
colorFrom: blue
colorTo: blue
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# ✅ Running Backend Locally

## 1. Clone the repository

```bash
git clone https://github.com/Monson2002/SHL-Assessment-Recommendation-Engine.git
cd SHL-Assessment-Recommendation-Engine
```

## 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install --no-cache-dir -r requirements.txt
```

## 4. Build the RAG corpus (first time only)

```bash
python src/rag_corpus.py
```
This loads the scraped SHL assessment data and prepares the RAG dataset.

```bash
python .\main_backup.py 
```

## 5. Run the backend server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```