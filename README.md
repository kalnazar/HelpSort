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

Running tests

```bash
pytest
```

Notes about tests:

- Some tests in `tests/` reference model-loading behavior and may fail if required model artifacts or optional dependencies (e.g., heavy transformer tooling) are not available. Consider running tests with mocks or skipping expensive tests in CI.

Production / deployment notes

- For production serve the Flask app behind a production WSGI server such as Gunicorn. Example (from project root):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 server.app:app
```

- Tune worker count according to CPU. Use process managers (systemd, Docker, Kubernetes) for stability.
- Restrict CORS origins in production: currently the app enables broad CORS; tighten to allowed domains.

Security & operational tips

- Rate limiting (`Flask-Limiter`) is configured with conservative defaults — adjust as needed.
- Avoid committing large model files or datasets to source control. Use the provided `.gitignore`.

Troubleshooting

- If `python server/app.py` fails with missing model files, check `server/models/model_schema/trained_models/` and run the training scripts.
- If frontend cannot reach the backend, verify `client/.env`'s `VITE_API_BASE_URL` and that the backend is running and accessible.

Contributing

- Please open issues or pull requests. For training data changes, provide data source and license information.

License & authors

- Created by students of KBTU as a Bachelor's Diploma Project.

If you'd like, I can also add badges, a `CONTRIBUTING.md`, or a short `deploy.md` with a Dockerfile example.
