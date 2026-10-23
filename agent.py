
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool
from langchain.agents import create_agent


# 1. Load environment variables
load_dotenv()

# 2. Initialize Groq
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


# 3. Load the same embedding model used during ingestion
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Connect to the existing vector database
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# 5. Create a retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# 6. Expose document search as an agent tool
@tool
def search_documents(question: str) -> str:
    """Search indexed documents for information relevant to a question.
    Use this tool when answering questions about the user's documents.
    """
    documents = retriever.invoke(question)

    if not documents:
        return "No relevant documents were found."

    results = []

    for doc in documents:
        source = doc.metadata.get("source", "Unknown source")
        results.append(
            f"Source: {source}\nContent: {doc.page_content}"
        )

    return "\n\n".join(results)


# 7. Create the agent
agent = create_agent(
    model=llm,
    tools=[search_documents],
    system_prompt=(
        "You are an AI Document Assistant. "
        "Use the search_documents tool for questions about document content. "
        "Base factual answers on the retrieved document content. "
        "If the documents do not contain the answer, clearly say "
        "that you could not find the information. "
        "Do not invent facts or claim that you searched documents "
        "unless you used the search tool."
    )
)


# 8. Run a conversation loop
def main():
    print("AI Document Agent is ready!")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        result = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        })

        # The last message contains the agent's final response
        print("\nAssistant:")
        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
