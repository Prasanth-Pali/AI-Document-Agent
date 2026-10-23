
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# 1. Define the document and vector database locations
DOCUMENTS_DIR = Path("documents")
CHROMA_DIR = "chroma_db"


def main():
    # 2. Load all TXT files from the documents folder
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        loaded_documents = loader.load()
        documents.extend(loaded_documents)

    if not documents:
        print("No TXT documents found in the documents folder.")
        return

    print(f"Loaded {len(documents)} document(s).")

    # 3. Split document text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # 4. Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 5. Store document chunks and embeddings in ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print(f"Successfully indexed {len(chunks)} chunks.")
    print(f"Vector database location: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
