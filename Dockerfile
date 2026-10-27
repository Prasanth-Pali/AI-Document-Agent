# ---------- Stage 1: build the Angular frontend ----------
FROM node:22-alpine AS frontend
WORKDIR /ui
COPY ai-document-agent-ui/package*.json ./
RUN npm install
COPY ai-document-agent-ui/ ./
RUN npm run build
RUN mkdir /out && cp -r dist/*/browser/. /out/

# ---------- Stage 2: Python backend ----------
FROM python:3.11-slim
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    API_BASE_URL=http://127.0.0.1:7860
WORKDIR /home/user/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

COPY --chown=user *.py ./
COPY --chown=user documents ./documents
COPY --chown=user --from=frontend /out ./static
RUN mkdir -p uploads chroma_db

EXPOSE 7860
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]