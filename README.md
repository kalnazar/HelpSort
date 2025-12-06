# HelpSort — NLP-Based Ticket Classification & Routing System

HelpSort is an end-to-end NLP platform for automatic classification, prioritization, and routing of support tickets.

**Status:** prototype / research — TF‑IDF based classifiers included. Training scripts and data preprocessing are provided.

**Repository root layout (important files/folders):**

- `client/` — React frontend (Vite)
- `server/` — Flask API, training scripts, model utilities
- `data/` — training and validation CSVs
- `server/models/model_schema/trained_models/` — pre-saved model artifacts (some may be committed)
- `requirements.txt` — Python dependencies

Prerequisites

- Python 3.11 (recommended)
- Node.js >= 16 (or compatible LTS)
- git

Quick start — local development

1. Clone repository

```bash
git clone <repo-url>
cd HelpSort
```

2. Backend (Flask)

```bash
# create and activate virtual env
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip and install deps
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# run backend (development)
python server/app.py
```

Default backend URL: `http://127.0.0.1:5000`

Notes:

- The backend expects model artifacts under `server/models/model_schema/trained_models/`. Pretrained TF‑IDF models may already be included. If they are missing, run training scripts (see below).
- Limit the maximum request body size or add input sanitization if you expect untrusted uploads.

3. Frontend (client)

```bash
cd client
npm install
# set API base URL for dev
echo "VITE_API_BASE_URL=http://127.0.0.1:5000" > .env
npm run dev
```

Open the dev server (Vite) URL shown in the terminal (usually `http://localhost:5173`). The frontend will call the Flask API at the address in `client/.env`.

Training models (optional)

If you want to (re)train the TF‑IDF models locally, run the scripts from the repo root:

```bash
python server/training/train_topic_tfidf.py
python server/training/train_priority_tfidf.py
python server/training/train_routing_tfidf.py
```

Training scripts read CSV files in `data/` (examples: `data/topic_train.csv`, `data/topic_val.csv`, etc.). See `data/README.txt` for CSV schema details and preprocessing notes.

Authors

- Created by students of KBTU as a Bachelor's Diploma Project.
