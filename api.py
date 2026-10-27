
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
import traceback
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import answer_question
from ingest import (
    ALLOWED_EXTENSIONS,
    DOCUMENTS_DIR,
    UPLOADS_DIR,
    index_file
)
import os
from fastapi.staticfiles import StaticFiles



app = FastAPI(
    title="AI Document Assistant API",
    description="Upload documents and ask questions about their content.",
    version="1.0.0"
)
if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Document Assistant API is running"}


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
            detail="File size must not exceed 10 MB."
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

    documents = []

    # Existing local/sample documents.
    for file_path in DOCUMENTS_DIR.rglob("*"):
        if (
            not file_path.is_file()
            or file_path.suffix.lower() not in ALLOWED_EXTENSIONS
        ):
            continue

        stat = file_path.stat()

        documents.append({
            "document_id": f"local-{file_path.name}",
            "filename": file_path.name,
            "file_type": file_path.suffix.lower(),
            "size_bytes": stat.st_size,
            "location": "local",
            "uploaded_at": datetime.fromtimestamp(
                stat.st_mtime, timezone.utc
            ).isoformat()
        })

    # Original files uploaded through the UI.
    for file_path in UPLOADS_DIR.glob("*/*"):
        if (
            not file_path.is_file()
            or file_path.suffix.lower() not in ALLOWED_EXTENSIONS
        ):
            continue

        stat = file_path.stat()

        documents.append({
            "document_id": file_path.parent.name,
            "filename": file_path.name,
            "file_type": file_path.suffix.lower(),
            "size_bytes": stat.st_size,
            "location": "uploaded",
            "uploaded_at": datetime.fromtimestamp(
                stat.st_mtime, timezone.utc
            ).isoformat()
        })

    documents.sort(
        key=lambda document: document["filename"].lower()
    )

    return {
        "total_documents": len(documents),
        "documents": documents
    }





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
