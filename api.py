import base64
import os
import secrets
import threading
import traceback
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent import answer_question
from document_list import build_document_list
from ingest import (
    ALLOWED_EXTENSIONS,
    UPLOADS_DIR,
    index_file,
    index_if_empty
)

# Read after the imports so values from .env are already loaded.
APP_PASSWORD = os.getenv("APP_PASSWORD", "")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Index the sample documents in the background if the index is empty.
    threading.Thread(target=index_if_empty, daemon=True).start()
    yield


app = FastAPI(
    title="AI Document Assistant API",
    description="Upload documents and ask questions about their content.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def basic_auth(request: Request, call_next):
    """Ask for a password on every route when APP_PASSWORD is set."""

    if (
        not APP_PASSWORD
        or request.method == "OPTIONS"
        or request.url.path == "/health"
    ):
        return await call_next(request)

    header = request.headers.get("Authorization", "")

    if header.startswith("Basic "):
        try:
            decoded = base64.b64decode(header[6:]).decode("utf-8")
            _, _, password = decoded.partition(":")

            if secrets.compare_digest(
                password.encode("utf-8"),
                APP_PASSWORD.encode("utf-8")
            ):
                return await call_next(request)
        except Exception:
            pass

    return Response(
        content="Authentication required",
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="AI Document Agent"'}
    )


class ChatRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Save an original file and index its contents."""

    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if not filename or extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Supported file types: PDF, DOCX, CSV and TXT."
        )

    try:
        file_bytes = await file.read(MAX_FILE_SIZE + 1)
    finally:
        await file.close()

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 5 MB."
        )

    # Each upload receives a unique ID and its own folder.
    document_id = uuid4().hex
    document_folder = UPLOADS_DIR / document_id
    file_path = document_folder / filename

    try:
        document_folder.mkdir(parents=True, exist_ok=False)
        file_path.write_bytes(file_bytes)

        # Read the saved file, split its content and store embeddings.
        chunk_count = index_file(
            file_path=file_path,
            document_id=document_id,
            source_filename=filename
        )

    except Exception as exc:
        # Avoid leaving an incomplete file after an indexing failure.
        if file_path.exists():
            file_path.unlink()

        if document_folder.exists():
            document_folder.rmdir()

        raise HTTPException(
            status_code=400,
            detail=f"Could not process and index the document: {exc}"
        ) from exc

    return {
        "document_id": document_id,
        "filename": filename,
        "file_type": extension,
        "size_bytes": len(file_bytes),
        "chunks_indexed": chunk_count,
        "message": "File saved and indexed successfully."
    }


@app.get("/api/documents")
def list_documents():
    """List local sample documents and files uploaded through the UI."""

    return build_document_list()


@app.post("/api/chat")
def chat(request: ChatRequest):
    """Ask the Agent a question about the available documents."""

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        answer = answer_question(request.question)

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as exc:
        print("\n========== AI AGENT ERROR ==========")
        traceback.print_exc()
        print("====================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


# Serve the built Angular app. This MUST stay at the bottom, after all routes.
if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
else:

    @app.get("/")
    def home():
        return {"message": "AI Document Assistant API is running"}