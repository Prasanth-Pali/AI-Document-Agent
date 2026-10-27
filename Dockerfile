# ---------- Stage 1: build the Angular frontend ----------
FROM node:22-alpine AS frontend
WORKDIR /ui
COPY ai-document-agent-ui/package*.json ./
RUN npm install
COPY ai-document-agent-ui/ ./
RUN npm run build
RUN mkdir /out && cp -r dist/*/browser/. /out/

# ---------- Stage 2: Python backend (no PyTorch) ----------
FROM python:3.11-slim
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    EMBEDDING_CACHE_DIR=/home/user/models
WORKDIR /home/user/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the small embedding model at build time so startup is fast
RUN python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='sentence-transformers/all-MiniLM-L6-v2', cache_dir='/home/user/models')"

COPY --chown=user *.py ./
COPY --chown=user documents ./documents
COPY --chown=user --from=frontend /out ./static
RUN mkdir -p uploads chroma_db

EXPOSE 7860
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-7860}"]