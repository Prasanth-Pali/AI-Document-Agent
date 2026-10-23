# 🤖 AI Document Agent

An AI-powered document assistant built with **Python, LangChain, Groq, Hugging Face Embeddings, ChromaDB, and FastAPI**. The application allows users to upload documents, index their contents, search for relevant information, and ask natural-language questions answered using the uploaded documents.

## ✨ Features

- 📄 **Multi-format document support** — PDF, DOCX, TXT, and CSV.
- 📂 **File storage** — saves original uploaded files in a local `uploads/` directory.
- 🧩 **Document processing** — extracts text and splits it into manageable chunks.
- 🔢 **Text embeddings** — uses `sentence-transformers/all-MiniLM-L6-v2` to convert text into vector representations.
- 🗄️ **Vector database** — stores document chunks, embeddings, and metadata in persistent ChromaDB.
- 🔍 **Semantic search** — retrieves relevant document chunks based on the user's question.
- 🧠 **LLM integration** — uses a Groq-hosted language model to generate responses.
- 🛠️ **LangChain Agent and tools** — provides `get_documents` and `search_documents` tools.
- 🚀 **REST API** — FastAPI endpoints for document upload, document listing, and AI chat.
- 🔗 **Source-aware responses** — retrieves source filenames and document metadata alongside relevant content.

## 🏗️ Architecture

```text
                    User / Client
                         |
                         v
                  FastAPI Backend
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
          Upload       List        Chat
             |          API         API
             v                       |
       Save Original                  v
       File to uploads/          LangChain Agent
             |                       |
             v                +------+------+
       Extract Text           |             |
             |                v             v
             v          get_documents  search_documents
       Split into Chunks       |             |
             |                 v             v
             v            FastAPI GET    ChromaDB
       Hugging Face          Endpoint    Vector Search
       Embeddings                            |
             |                               |
             v                               v
          ChromaDB <---------------- Retrieved Chunks
                                             |
                                             v
                                       Groq LLM
                                             |
                                             v
                                      Final Answer
```

### 🔄 RAG Pipeline

The Retrieval-Augmented Generation (RAG) pipeline follows these stages:

1. **Load:** Read a document from disk and extract its text.
2. **Split:** Divide the extracted text into overlapping chunks.
3. **Embed:** Generate vector embeddings using the Hugging Face embedding model.
4. **Store:** Persist chunks, vectors, and metadata in ChromaDB.
5. **Retrieve:** Find relevant chunks using semantic similarity search.
6. **Generate:** Provide the retrieved context to the LLM to produce an answer.

Documents uploaded through the API are indexed during the upload process. The embedding model runs locally, while the LLM is accessed through Groq's API.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application language |
| LangChain | Agent creation, tools, prompts, and RAG orchestration |
| Groq | Hosted LLM inference |
| Hugging Face Sentence Transformers | Local text embeddings |
| ChromaDB | Persistent vector storage and similarity search |
| FastAPI | REST API backend |
| Pydantic | API request validation |
| PyPDF | PDF text extraction |
| docx2txt | Word document text extraction |
| Python CSV | CSV text extraction |

## 📁 Project Structure

```text
AI-Document-Agent/
│
├── documents/          # Existing local/sample documents
├── uploads/            # Original files uploaded through the API
│   └── <document-id>/
│       └── document.pdf
│
├── chroma_db/          # Persistent vector database
│
├── api.py              # FastAPI upload, list, and chat endpoints
├── ingest.py           # Text extraction, chunking, and indexing
├── tools.py            # LangChain document tools
├── agent.py            # LLM-powered Agent
├── app.py              # Basic RAG implementation
│
├── requirements.txt
├── .env                # API credentials and configuration
├── .gitignore
└── README.md
```

### 📌 Main Components

- **`api.py`** — exposes REST endpoints and saves uploaded files before indexing them.
- **`ingest.py`** — extracts document text, creates chunks, generates embeddings, and stores them in ChromaDB.
- **`tools.py`** — implements `get_documents()` for listing files and `search_documents()` for searching document contents.
- **`agent.py`** — creates the LangChain Agent and integrates it with the Groq LLM.
- **`app.py`** — demonstrates a basic RAG pipeline without Agent tool selection.

## ⚙️ Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies.
- A Groq API key.
- Internet connectivity for Groq API requests and the initial download of the embedding model.
- Git for version control.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Prasanth-Pali/AI-Document-Agent.git
cd AI-Document-Agent
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model
API_BASE_URL=http://127.0.0.1:8000
```

Replace the placeholder values with your actual configuration. Never commit API credentials to GitHub.

### 5. Prepare Documents

Place existing sample documents inside the `documents/` directory.

Supported file formats:

- PDF (`.pdf`)
- Microsoft Word (`.docx`)
- Text (`.txt`)
- Comma-separated values (`.csv`)

To index local sample documents and previously saved uploads, run:

```bash
python ingest.py
```

This step is useful when indexing local files or rebuilding the index. Files uploaded through the API are indexed automatically.

### 6. Start the FastAPI Server

```bash
uvicorn api:app --reload
```

Open the interactive API documentation:

**http://127.0.0.1:8000/docs**

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| GET | `/health` | Health check |
| POST | `/api/documents/upload` | Upload, save, and index a document |
| GET | `/api/documents` | List local and uploaded documents |
| POST | `/api/chat` | Ask a question using the AI Agent |

### 📤 Upload a Document

Use `POST /api/documents/upload` with a multipart form field named `file`.

The endpoint:

1. Validates the file extension and size.
2. Saves the original file under `uploads/<document-id>/`.
3. Extracts its text.
4. Splits the text into chunks and generates embeddings.
5. Stores the chunks and metadata in ChromaDB.
6. Returns the document ID and indexing details.

The configured maximum file size is 10 MB.

### 📚 List Documents

Call `GET /api/documents`.

The response includes information such as:

- Document ID
- Filename
- File type
- File size
- Storage location
- File modification or upload timestamp

This endpoint lists original files from the `documents/` and `uploads/` directories.

### 💬 Ask a Question

Call `POST /api/chat` with a JSON request body:

```json
{
  "question": "What does the company leave policy say?"
}
```

The Agent selects the appropriate tool, retrieves relevant information when necessary, and uses the LLM to formulate a response.

## 🛠️ Agent Tools

### 1. `get_documents()`

Retrieves the available document list through the FastAPI GET endpoint.

Example user question:

> Which documents are available?

The tool returns document metadata for the Agent to interpret.

### 2. `search_documents(question, document_id="")`

Searches the ChromaDB collection using vector similarity.

- `question` specifies the information to find.
- `document_id` optionally restricts the search to one indexed document.
- An empty document ID searches across the collection.

Example user question:

> What are the eligibility requirements mentioned in the policy?

The tool retrieves relevant chunks and their source metadata. The Agent uses those results to formulate its answer.

## 🗃️ Storage Design

The project uses two separate types of storage.

**Original files — `documents/` and `uploads/`**

These directories contain the source files from which text is extracted.

**Vector database — `chroma_db/`**

ChromaDB stores the extracted text chunks, vector embeddings, and associated metadata.

Original files are not stored inside ChromaDB. The vector database supports semantic retrieval, while the filesystem preserves the source documents.

## 🔐 Security and Limitations

- Keep API keys in environment variables.
- Do not commit `.env`, uploaded files, or the local vector database.
- The current local filesystem design is intended for development and learning.
- Scanned PDFs may require OCR because ordinary PDF text extraction does not recognize text in images.
- The current design does not implement user authentication or per-user document isolation.
- Production deployments should add stronger file validation, upload limits, access controls, safe error handling, and reliable rollback or cleanup for failed indexing operations.
- Semantic search results depend on document quality, chunking, embeddings, and retrieval settings.

## 🗺️ Future Enhancements

- 🖥️ Angular UI for document upload, document listing, and chat.
- 📑 Display source documents and relevant text snippets alongside answers.
- 🗑️ Delete documents and their corresponding vector records.
- 🔄 Re-index updated files and handle duplicate uploads reliably.
- 🔒 Authentication and user-specific document access.
- 🐳 Docker containerization.
- ☁️ Cloud deployment and CI/CD integration.
- 📊 Logging, monitoring, and improved API error handling.

## 👨‍💻 Author

**Pali Prasanth**

- GitHub: https://github.com/Prasanth-Pali
- Project Repository: https://github.com/Prasanth-Pali/AI-Document-Agent

---

*Built to explore LLM integration, LangChain agents, tool calling, embeddings, vector databases, and Retrieval-Augmented Generation (RAG) in a practical Python application.*
