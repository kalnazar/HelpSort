# HelpSort — Frontend (React + Vite)

This folder contains the React frontend built with Vite. The app is a lightweight UI to submit support ticket text and show predicted topic, priority and routing.

Prerequisites

- Node.js >= 16
- npm (or yarn/pnpm)

Local development

1. Install dependencies

```bash
cd client
npm install
```

2. Configure API base URL (dev)

Create `client/.env` with:

```bash
VITE_API_BASE_URL=http://127.0.0.1:5000
```

3. Start dev server

```bash
npm run dev
```

Build & preview

```bash
npm run build
npm run preview
```

API endpoints used by the frontend

- `POST /classify` — classify ticket text; request body: `{ "text": "..." }`.
- `GET /load_model` — (optional) load models.
- `POST /select_model` — (optional) select model variant.

Notes

- The frontend reads `VITE_API_BASE_URL` at build/dev time. Ensure the backend is running and reachable at that address.
- If you prefer a different port for the Flask backend, update `client/.env` accordingly.

If you'd like, I can add `npm` scripts for linting & formatting, or convert the project to TypeScript.
