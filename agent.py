
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools import get_documents, search_documents


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[
        get_documents,
        search_documents
    ],
    system_prompt="""
You are an AI Document Assistant.

Your job is to answer questions using the user's available documents.

Rules:
1. If the user asks which documents are available, use get_documents.
2. If the user asks about information inside a document, use search_documents.
3. If the user names a specific document, call get_documents first
   when you need to identify its document ID, then search that document.
4. For a general question about document contents, search across all
   indexed documents.
5. Do not invent facts that are not supported by retrieved content.
6. If the retrieved content does not contain the answer, clearly say so.
7. Mention the source filename when answering from a document.
8. Never claim a file was uploaded or indexed unless the available
   tool results support that claim.
"""
)


def answer_question(question: str) -> str:
    """Run the Agent and return its final answer."""

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    messages = result.get("messages", [])

    if not messages:
        return "The Agent did not return an answer."

    answer = messages[-1].content

    if isinstance(answer, str):
        return answer

    return str(answer)


if __name__ == "__main__":
    print("AI Document Agent is ready. Type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            print("\nAssistant:", answer_question(question))
        except Exception as exc:
            print(f"\nError: {exc}")
