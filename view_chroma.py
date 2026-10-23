from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load the same embedding model used during ingestion
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to the existing ChromaDB
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# Retrieve stored documents and embeddings
data = vector_store.get(
    include=["documents", "embeddings", "metadatas"]
)

print("Total records:", len(data["ids"]))

# Display the first record
if data["ids"]:
    print("\nDocument:")
    print(data["documents"][0])

    print("\nEmbedding:")
    print(data["embeddings"][0])

    print("\nEmbedding dimensions:")
    print(len(data["embeddings"][0]))

    print("\nMetadata:")
    print(data["metadatas"][0])