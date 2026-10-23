
import csv
import io
from pathlib import Path

import docx2txt
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = BASE_DIR / "documents"
UPLOADS_DIR = BASE_DIR / "uploads"
CHROMA_DIR = str(BASE_DIR / "chroma_db")

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".csv", ".txt"}

# Create the required directories if they don't exist.
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Embedding model: runs locally.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# All documents use the same persistent ChromaDB collection.
vector_store = Chroma(
    collection_name="uploaded_documents",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


def extract_text(file_path: Path) -> str:
    """Extract readable text from a supported document."""

    extension = file_path.suffix.lower()

    if extension == ".txt":
        return file_path.read_text(encoding="utf-8-sig")

    if extension == ".pdf":
        reader = PdfReader(str(file_path))
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if extension == ".docx":
        return docx2txt.process(str(file_path)) or ""

    if extension == ".csv":
        csv_text = file_path.read_text(encoding="utf-8-sig")
        rows = csv.reader(io.StringIO(csv_text))

        return "\n".join(
            " | ".join(row)
            for row in rows
        )

    raise ValueError(f"Unsupported file type: {extension}")


def index_file(
    file_path: Path,
    document_id: str,
    source_filename: str
) -> int:
    """Extract text, create chunks and store embeddings in ChromaDB."""

    text = extract_text(file_path)

    if not text.strip():
        raise ValueError(
            "No readable text was found in the document."
        )

    text_chunks = text_splitter.split_text(text)

    if not text_chunks:
        raise ValueError("No text chunks were generated.")

    # Replace any existing chunks belonging to this document ID.
    vector_store.delete(
        where={"document_id": document_id}
    )

    documents = []
    ids = []

    for index, chunk in enumerate(text_chunks):
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "document_id": document_id,
                    "source": source_filename,
                    "file_type": file_path.suffix.lower(),
                    "chunk_index": index
                }
            )
        )

        # Stable chunk IDs prevent duplicate chunks on re-indexing.
        ids.append(f"{document_id}-chunk-{index}")

    vector_store.add_documents(
        documents=documents,
        ids=ids
    )

    return len(documents)


def index_local_documents() -> None:
    """Index local sample documents and saved UI uploads."""

    files_to_index = []

    # Existing local/sample files.
    for file_path in DOCUMENTS_DIR.rglob("*"):
        if (
            file_path.is_file()
            and file_path.suffix.lower() in ALLOWED_EXTENSIONS
        ):
            document_id = f"local-{file_path.name}"
            files_to_index.append(
                (file_path, document_id, file_path.name)
            )

    # UI-uploaded files are stored as uploads/<document_id>/<filename>.
    for file_path in UPLOADS_DIR.glob("*/*"):
        if (
            file_path.is_file()
            and file_path.suffix.lower() in ALLOWED_EXTENSIONS
        ):
            document_id = file_path.parent.name
            files_to_index.append(
                (file_path, document_id, file_path.name)
            )

    for file_path, document_id, filename in files_to_index:
        try:
            count = index_file(
                file_path,
                document_id,
                filename
            )
            print(f"Indexed {filename}: {count} chunks")

        except Exception as exc:
            print(f"Failed to index {filename}: {exc}")


if __name__ == "__main__":
    index_local_documents()
