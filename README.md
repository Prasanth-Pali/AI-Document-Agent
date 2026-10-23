# 📄 AI Document Agent

An AI-powered document question-answering application that allows users to upload documents and ask natural-language questions about their content. The application uses **Retrieval-Augmented Generation (RAG)**, LangChain tools, an LLM, and vector search to retrieve relevant information and generate contextual answers.

## ✨ Features

- 📤 **Document Upload** — Upload PDF, DOCX, CSV, and TXT files.
- 🔍 **Document Processing** — Extract text, split it into manageable chunks, and generate embeddings.
- 🧠 **RAG Pipeline** — Retrieve relevant document chunks to provide context-aware answers.
- 🤖 **AI Agent** — Use LangChain tools to retrieve document information and support question answering.
- 💬 **AI Chat Interface** — Ask questions in natural language and view generated answers.
- 🗂️ **Document Management** — View uploaded documents and their metadata.
- 🧮 **Vector Search** — Store and search document embeddings using ChromaDB.
- ⚡ **FastAPI Backend** — Expose REST APIs for document upload, retrieval, and AI chat.
- 🎨 **Angular Dashboard** — Responsive dashboard with a red-and-blue theme.
- 🔐 **Environment-Based Configuration** — Store API credentials outside the source code.
- 💾 **Persistent Vector Storage** — Retain indexed document vectors locally between application restarts.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | Angular, TypeScript, HTML, CSS |
| Backend | Python, FastAPI |
| AI Framework | LangChain |
| Language Model | Groq-hosted LLM through `ChatGroq` |
| Embeddings | Hugging Face Sentence Transformers |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| Document Processing | PyPDF, docx2txt, Python CSV processing |
| API Communication | REST APIs, HTTP, JSON |
| Environment Configuration | Python dotenv |

## 🏗️ Architecture

```text
┌──────────────────────────────┐
│       Angular Dashboard      │
│                              │
│  Upload Documents            │
│  View Uploaded Documents     │
│  Ask Questions               │
└──────────────┬───────────────┘
               │ HTTP / REST
               ▼
┌──────────────────────────────┐
│        FastAPI Backend       │
│                              │
│  Document Upload API         │
│  Document Listing API        │
│  AI Chat API                 │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌────────────────┐
│ Document     │  │ LangChain      │
│ Ingestion    │  │ AI Agent       │
└──────┬───────┘  └───────┬────────┘
       │                  │
       ▼                  ▼
┌──────────────┐  ┌────────────────┐
│ Hugging Face │  │ LangChain      │
│ Embeddings   │  │ Document Tools │
└──────┬───────┘  └───────┬────────┘
       │                  │
       ▼                  ▼
┌──────────────┐  ┌────────────────┐
│ ChromaDB     │  │ Document Search│
│ Vector Store │  │ and Retrieval  │
└──────────────┘  └───────┬────────┘
                          ▼
                  ┌────────────────┐
                  │ Groq LLM        │
                  │ Answer Generation│
                  └────────────────┘
```

## 🔄 How It Works

### 1. Document Upload

The user uploads a supported document through the Angular dashboard. The frontend sends the file to the FastAPI backend using a multipart HTTP request.

### 2. Text Extraction and Chunking

The backend extracts text from the uploaded document. The text is divided into smaller chunks using `RecursiveCharacterTextSplitter`.

Current chunking configuration:

- Chunk size: `500` characters
- Chunk overlap: `100` characters

Chunking allows the application to index and retrieve relevant sections instead of processing an entire document at once.

### 3. Embedding Generation

The application uses the Hugging Face embedding model `sentence-transformers/all-MiniLM-L6-v2` to convert document chunks into vector representations.

The embedding model runs locally.

### 4. Vector Storage

The generated embeddings and associated document metadata are stored in a persistent ChromaDB collection named `uploaded_documents`.

### 5. Question Processing

When the user submits a question, the AI agent can use its LangChain tools to retrieve document information and search the vector database for relevant content.

### 6. Context Retrieval and Answer Generation

The retrieved document chunks provide context for answering the user's question. The Groq-hosted language model generates the final natural-language response.

### 7. Response Display

FastAPI returns the answer to the Angular frontend, which displays it in the chat interface.

## 📁 Project Structure

```text
AI-Document-Agent/
│
├── documents/
│   └── company_policy.txt
│
├── uploads/
│   └── Uploaded documents
│
├── chroma_db/
│   └── Persistent vector database
│
├── ai-document-agent-ui/
│   ├── src/
│   │   └── app/
│   │       ├── pages/
│   │       │   └── dashboard/
│   │       │       ├── dashboard.component.ts
│   │       │       ├── dashboard.component.html
│   │       │       └── dashboard.component.css
│   │       ├── services/
│   │       │   └── document.ts
│   │       ├── app.ts
│   │       ├── app.html
│   │       └── app.config.ts
│   ├── package.json
│   └── angular.json
│
├── .env
├── .gitignore
├── requirements.txt
├── ingest.py
├── tools.py
├── agent.py
├── app.py
├── api.py
└── README.md
```

**Note:** `uploads/`, `chroma_db/`, and `.env` are local runtime resources and should not be committed to GitHub. The structure above describes the intended layout; generated files and local folders may differ.

## ⚙️ Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version supported by the installed dependencies
- Node.js and npm
- Angular CLI
- A Groq API key
- Git

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Prasanth-Pali/AI-Document-Agent.git
cd AI-Document-Agent
```

### 2. Set Up the Python Backend

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the backend project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model
API_BASE_URL=http://127.0.0.1:8000
```

Replace the example values with your own credentials and a Groq-supported model identifier.

**Security:** Never commit your real API key to GitHub. Keep `.env` in `.gitignore`.

### 4. Start the FastAPI Backend

From the directory containing `api.py`, run:

```bash
uvicorn api:app --reload
```

The backend runs at:

- API base URL: `http://127.0.0.1:8000`
- Swagger documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

### 5. Start the Angular Frontend

Open a second terminal:

```bash
cd ai-document-agent-ui
npm install
ng serve
```

Open the dashboard:

`http://localhost:4200`

Keep both the FastAPI backend and Angular development server running while using the application.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/documents` | Retrieve the uploaded document list |
| `POST` | `/api/documents/upload` | Upload and index a document |
| `POST` | `/api/chat` | Submit a question to the AI agent |

### Upload a Document

Endpoint: `POST /api/documents/upload`

Content type: `multipart/form-data`

Form field: `file`

Supported formats: PDF, DOCX, CSV, and TXT.

### Retrieve Documents

Endpoint: `GET /api/documents`

Returns document metadata such as document ID, filename, file type, size, and upload information.

### Ask a Question

Endpoint: `POST /api/chat`

Example request:

```json
{
  "question": "What is the company's leave policy?"
}
```

The response contains the submitted question and the generated answer. Exact response fields depend on the backend implementation.

## 🧪 Development Notes

- Uploaded documents are indexed by the ingestion pipeline.
- `ingest.py` can also be used to index local sample documents when supported by its current implementation.
- `tools.py` contains the document retrieval tools used by the agent.
- `agent.py` handles the LangChain agent workflow.
- `app.py` is a separate basic RAG demonstration; the Angular application communicates with `api.py`.
- ChromaDB stores vector data, while the original uploaded files are stored separately.
- The current chat interface displays the latest answer; persistent conversations and chat history are not yet implemented.

## 🔮 Future Enhancements

- 💬 Conversation history with multiple messages per chat.
- 💾 Persistent chat and message storage.
- 🗃️ Document-specific question answering and filtering.
- 📚 Source citations showing which document sections support an answer.
- 🔐 Authentication and user-specific document access.
- 🧹 Document deletion with corresponding vector-store cleanup.
- 🐳 Docker containerization.
- 🚀 CI/CD with GitHub Actions.
- ☁️ Deployment to a cloud platform.
- 📝 Improved error handling, logging, and monitoring.
- 🧪 Automated backend and frontend tests.

## 🔒 Security Considerations

- Store credentials in environment variables.
- Validate file extensions, content, and file sizes on the server.
- Restrict access to uploaded documents and vector data.
- Configure CORS for trusted frontend origins.
- Add authentication and authorization before exposing the application publicly.
- Avoid logging API keys, confidential document contents, or sensitive user information.

## 👨‍💻 Author

**Prasanth Pali**

GitHub: [Prasanth-Pali](https://github.com/Prasanth-Pali)

---

*Built to explore document ingestion, embeddings, vector search, RAG, LangChain agents, FastAPI, and Angular integration in a practical AI application.*
