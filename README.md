# AI Document RAG Agent 🤖

An AI-powered document assistant built with **Python, LangChain, Groq, Hugging Face Embeddings, and ChromaDB**. It retrieves relevant information from documents and uses an LLM to answer questions based on the retrieved content.

The project demonstrates a basic **Retrieval-Augmented Generation (RAG) pipeline** and an AI agent that can search indexed documents using a custom LangChain tool.

## ✨ Features

- 📄 Load and process text documents (`.txt`)
- ✂️ Split documents into smaller chunks with overlap
- 🧠 Generate embeddings using Hugging Face
- 🗄️ Store and retrieve document embeddings using ChromaDB
- 🔍 Perform semantic search on indexed documents
- 💬 Generate context-aware answers using the Groq LLM
- 🛠️ Create a custom document-search tool using LangChain's `@tool`
- 🤖 Build an AI agent using LangChain's `create_agent()`
- 🔐 Load API credentials securely from environment variables

## 🏗️ Architecture

```text
                Text Documents
                      |
                      v
                  ingest.py
                      |
             Load and Split Text
                      |
                      v
             Hugging Face Embeddings
                      |
                      v
                  ChromaDB
                      |
             Semantic Retrieval
                      |
                      v
User Question --> AI Agent / RAG Chain
                      |
                 Groq LLM
                      |
                      v
                Final Answer
```

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | LLM, RAG, tools, and agent orchestration |
| Groq | LLM inference |
| Hugging Face | Text embedding generation |
| Sentence Transformers | Local embedding model execution |
| ChromaDB | Vector storage and similarity search |
| python-dotenv | Environment variable management |

### Models

- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Chat model:** Configured through `ChatGroq` in the Python files. Use a model currently supported by your Groq account.

## 📁 Project Structure

```text
AI-Document-Agent/
│
├── documents/
│   └── company_policy.txt
│
├── chroma_db/           # Generated vector database
│
├── .env                 # API credentials (not committed)
├── .gitignore
├── requirements.txt
├── ingest.py             # Document loading and indexing
├── app.py                # Basic RAG question-answering pipeline
├── agent.py              # Tool-based AI document agent
└── README.md
```

## ⚙️ Prerequisites

- Python 3.10 or a compatible version supported by the installed packages
- A Groq API key
- Internet access for installing dependencies and downloading the embedding model

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Prasanth-Pali/AI-Document-Agent.git
cd AI-Document-Agent
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the placeholder with your own Groq API key. Never commit the `.env` file to GitHub.

### 5. Add documents

Place your sample `.txt` files inside the `documents/` directory.

The current ingestion script processes `.txt` files in that directory.

### 6. Index the documents

```bash
python ingest.py
```

This step loads the documents, splits the text into chunks, generates embeddings, and stores them in ChromaDB.

Run ingestion before using the RAG pipeline or agent.

### 7. Run the basic RAG application

```bash
python app.py
```

Ask questions about the indexed documents and receive answers based on the retrieved context.

### 8. Run the AI agent

```bash
python agent.py
```

The agent can decide to call the `search_documents` tool when it needs information from the indexed documents.

Type `exit` to stop the application.

## 💡 Example Questions

Using the sample company policy document, try asking:

- How many working days in advance should employees request annual leave?
- Who must approve a leave request?
- What information should an IT support ticket contain?
- What security precautions are required when working from home?
- What is the company's policy for sharing passwords?

If the requested information is not present in the documents, the assistant should state that it could not find the information rather than inventing an answer.

## 🔎 How RAG Works

Retrieval-Augmented Generation combines document retrieval with language-model generation.

1. **Load:** Read the source documents.
2. **Split:** Divide the documents into smaller text chunks.
3. **Embed:** Convert each chunk into a numerical vector.
4. **Store:** Save the vectors and associated text in ChromaDB.
5. **Retrieve:** Find relevant chunks for a user's question.
6. **Generate:** Provide the retrieved context to the LLM to produce an answer.

## 🤖 Basic RAG vs. AI Agent

| Basic RAG (`app.py`) | AI Agent (`agent.py`) |
|---|---|
| Follows a predefined retrieval-and-answer pipeline | Can decide when to use an available tool |
| Retrieves documents directly in application code | Uses the `search_documents` tool |
| Calls the LLM to answer using retrieved context | Uses the LLM to decide and formulate a response |
| Best for straightforward document Q&A | Demonstrates tool calling and agent orchestration |

## 🔐 Security and Best Practices

- Keep API keys in `.env`.
- Exclude `.env`, `.venv/`, `__pycache__/`, and `chroma_db/` from Git.
- Do not upload confidential company documents or sensitive business information.
- Use only documents you are authorized to process.
- Avoid repeatedly running ingestion against the same persistent collection without handling existing records; duplicate chunks can accumulate.

## 🔮 Future Enhancements

- Add PDF document ingestion and page-level source citations.
- Build a FastAPI service for the RAG pipeline.
- Add a web interface for document uploads and questions.
- Implement incremental document indexing and duplicate prevention.
- Add structured logging, error handling, and automated tests.
- Containerize the application with Docker.
- Add conversation history and document metadata filtering.

## 🎯 Learning Objectives

This project provides hands-on experience with:

- LLM integration using Groq
- Embeddings and semantic search
- Vector databases using ChromaDB
- Retrieval-Augmented Generation
- LangChain prompt templates and output parsing
- Custom tools using `@tool`
- AI agent creation using `create_agent()`

## 📜 License

👨‍💻 Author

Pali Prasanth

GitHub: Prasanth-Pali

Project: AI Document RAG Agent

Built to explore Retrieval-Augmented Generation (RAG), LangChain tools, AI agents, embeddings, and vector databases using Python and Groq.

This project is intended for learning and portfolio demonstration. Add a license file if you plan to distribute it under specific open-source terms.
