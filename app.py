
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. Load environment variables from .env
load_dotenv()

# 2. Initialize the Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


# 3. Initialize the same embedding model used during ingestion
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Connect to the existing ChromaDB
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# 5. Create a retriever to search for relevant chunks
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# 6. Define instructions for the LLM
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an AI Document Assistant.

Answer the user's question using only the provided context.
If the answer is not available in the context, say:
"I could not find this information in the provided documents."

Do not invent facts.

Context:
{context}"""
    ),
    ("human", "{question}")
])

# 7. Build the RAG chain
rag_chain = prompt | llm | StrOutputParser()


def main():
    question = input("\nAsk a question about your documents: ")

    # Retrieve relevant chunks from ChromaDB
    retrieved_docs = retriever.invoke(question)

    # Combine the retrieved text into one context string
    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    # Send the question and retrieved context to Groq
    answer = rag_chain.invoke({
        "context": context,
        "question": question
    })

    print("\nAnswer:")
    print(answer)

    print("\nSources:")
    for doc in retrieved_docs:
        print("-", doc.metadata.get("source", "Unknown source"))


if __name__ == "__main__":
    main()
