from datetime import datetime, timezone

from ingest import ALLOWED_EXTENSIONS, DOCUMENTS_DIR, UPLOADS_DIR


def build_document_list() -> dict:
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