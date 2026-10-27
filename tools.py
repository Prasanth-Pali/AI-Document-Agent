from langchain.tools import tool
import json

from document_list import build_document_list
from ingest import vector_store


@tool
def get_documents() -> str:
    """Get the list of available local and uploaded documents."""

    return json.dumps(build_document_list(), indent=2)


@tool
def search_documents(
    question: str,
    document_id: str = ""
) -> str:
    """
    Search document contents using vector similarity.

    Use question for the information to find.
    Use document_id to restrict the search to one document.
    Leave document_id empty to search across all indexed documents.
    """

    search_options = {"k": 4}

    if document_id.strip():
        search_options["filter"] = {
            "document_id": document_id.strip()
        }

    results = vector_store.similarity_search(
        question,
        **search_options
    )

    if not results:
        return "No relevant information was found in the indexed documents."

    formatted_results = []

    for document in results:
        source = document.metadata.get("source", "Unknown")
        source_id = document.metadata.get("document_id", "Unknown")
        chunk_index = document.metadata.get("chunk_index", "Unknown")

        formatted_results.append(
            f"Source: {source}\n"
            f"Document ID: {source_id}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n{document.page_content}"
        )

    return "\n\n---\n\n".join(formatted_results)