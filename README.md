# AI Document Agent

AI Document Agent is a document question-answering app. Upload PDF, DOCX, CSV, or TXT files, then ask questions about their contents through an Angular dashboard. A FastAPI backend extracts and chunks text, creates local embeddings, searches ChromaDB, and uses a Groq-hosted language model to generate answers.

## Features

- Upload supported documents up to **5 MB** each.
- Extract and chunk document text (500-character chunks with 100-character overlap).
- Create embeddings locally with `sentence-transformers/all-MiniLM-L6-v2` through FastEmbed.
- Store document chunks and metadata in a persistent ChromaDB collection.
- List sample and uploaded documents and ask questions through the web dashboard.
- Optionally protect API routes with HTTP Basic authentication using `APP_PASSWORD`.
- Serve the Angular production build from the FastAPI application.

## Architecture

```text
Angular dashboard
       │ HTTP
       ▼
FastAPI (api.py) ── LangChain agent/tools ── Groq API
       │
       ├── document extraction and local FastEmbed embeddings
       ├── ChromaDB (chroma_db/)
       └── original uploads (uploads/)
```

The embedding model runs locally; chat completions require a Groq API key and network access. The chat model is currently configured in `agent.py` as `openai/gpt-oss-20b`.

## Requirements

- Python 3.11
- Node.js 20 and npm (for frontend development or Docker builds)
- A Groq API key
- Docker Engine with Docker Compose (optional, for containerized use)

## Run locally

1. Clone the repository and enter its root directory:

   ```sh
   git clone https://github.com/Prasanth-Pali/AI-Document-Agent.git
   cd AI-Document-Agent
   ```

2. Create and activate a Python virtual environment, then install backend dependencies:

   ```sh
   python -m venv .venv
   ```

   PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```sh
   source .venv/bin/activate
   ```

   ```sh
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` in the repository root and set `GROQ_API_KEY`. In PowerShell, use `Copy-Item .env.example .env`; in macOS/Linux, use `cp .env.example .env`. `APP_PASSWORD` is optional; when non-empty, the API requires HTTP Basic authentication for all routes except `/health` and `OPTIONS`.

4. Start the API from the repository root:

   ```sh
   uvicorn api:app --reload
   ```

5. In another terminal, install and start the Angular development server:

   ```sh
   cd ai-document-agent-ui
   npm ci
   npm start
   ```

   Open <http://localhost:4200>. In development, the UI calls the API at `http://127.0.0.1:8000`.

The API is available at <http://127.0.0.1:8000>; interactive documentation is at `/docs` and `/redoc`. The public health endpoint is `/health`.

## Run with Docker Compose

1. Create `.env` in the repository root as described above and set `GROQ_API_KEY`. Set a strong `APP_PASSWORD` before exposing the service beyond a trusted local environment.
2. Build and start the app:

   ```sh
   docker compose up --build
   ```

3. Open <http://localhost:7860>. Stop the service with `Ctrl+C`; use `docker compose down` to remove the running container.

The image builds the Angular frontend and serves it from FastAPI. Compose persists uploaded originals, the ChromaDB index, and the embedding model cache in named volumes. To remove this data as well as the container, run `docker compose down --volumes`. The first image build downloads the embedding model and therefore needs network access.

To change the published port, set `HOST_PORT` (for example, `HOST_PORT=8080`) in `.env`; the app will then be available at `http://localhost:8080`.

To build and run without Compose:

```sh
docker build -t ai-document-agent .
docker run --rm -p 7860:7860 --env-file .env \
  -v ai-document-agent-uploads:/home/user/app/uploads \
  -v ai-document-agent-chroma:/home/user/app/chroma_db \
  -v ai-document-agent-models:/home/user/models \
  ai-document-agent
```

## API

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Health check (does not require `APP_PASSWORD`) |
| `GET` | `/api/documents` | List sample and uploaded documents |
| `POST` | `/api/documents/upload` | Upload and index a document (`multipart/form-data`, field `file`) |
| `POST` | `/api/chat` | Ask a question (`{"question": "..."}`) |

Uploaded file types are PDF, DOCX, CSV, and TXT. The server enforces the 5 MB limit regardless of client-side validation. FastAPI's interactive API documentation is available at `/docs`.

## Repository layout

```text
.
├── agent.py                    # LangChain agent and Groq model
├── api.py                      # FastAPI endpoints and static frontend hosting
├── app.py                      # Standalone RAG example
├── document_list.py            # Sample and uploaded document listing
├── ingest.py                   # Extraction, embedding, and ChromaDB indexing
├── tools.py                    # Agent tools for listing and searching documents
├── documents/                  # Sample documents indexed on first startup
├── ai-document-agent-ui/       # Angular application
├── Dockerfile                  # Multi-stage frontend/backend image
├── compose.yaml                # App service and persistent data volumes
└── requirements.txt            # Python dependencies
```

Runtime uploads, vector data, model cache, environment secrets, and frontend build output are local/container data and should not be committed. The root `.gitignore` and `.dockerignore` exclude generated and sensitive files.

## Development checks

Build the frontend:

```sh
cd ai-document-agent-ui
npm ci
npm run build
```

Run frontend unit tests in an environment with Chrome available:

```sh
npm test -- --watch=false --browsers=ChromeHeadless
```

From the repository root, check Python syntax with:

```sh
python -m compileall -q .
```

`app.py` is a standalone retrieval-chain example; the web UI uses `api.py` and the agent in `agent.py`. `view_chroma.py` is a local vector-store inspection utility.

## CI

GitHub Actions runs on pushes and pull requests targeting `main`, and can also be started manually from the Actions tab. The workflow builds and tests the Angular frontend and checks Python syntax. It does not build or publish a Docker image. Deployment is not configured.

## Security and data

- Keep `.env` private; never commit Groq credentials or a production password.
- Configure a strong `APP_PASSWORD` before exposing the service. Authentication is shared by the app and is not user-specific authorization.
- Uploaded files and the ChromaDB index are stored on local disk or in the configured Docker volumes. Back them up as needed and restrict access to the host.
- `/health` is intentionally unauthenticated. The API's CORS allowlist currently permits the Angular development origin `http://localhost:4200`.
- Do not use the sample configuration as a substitute for production security review or deployment hardening.

## License

No license file is currently included in this repository.
