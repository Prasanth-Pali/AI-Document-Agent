
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from ingest import vector_store

import os


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)

prompt = ChatPromptTemplate.from_template("""
You are an AI Document Assistant.

Answer the question using only the supplied context.
If the answer is not in the context, say you could not find it.
Mention the source filenames when possible.

Context:
{context}

Question:
{question}

Answer:
""")

chain = prompt | llm | StrOutputParser()


def ask_question(question: str) -> str:
    """Retrieve relevant chunks and generate an answer."""

    documents = retriever.invoke(question)

    if not documents:
        return "No relevant information was found in the documents."

    context_parts = []

    for document in documents:
        source = document.metadata.get("source", "Unknown")

        context_parts.append(
            f"Source: {source}\n"
            f"Content: {document.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    return chain.invoke({
        "context": context,
        "question": question
    })


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if question:
            print("\nAnswer:", ask_question(question))
