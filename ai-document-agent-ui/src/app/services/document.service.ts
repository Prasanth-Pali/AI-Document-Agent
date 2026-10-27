import { Injectable, inject, isDevMode } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UploadedDocument {
  document_id: string;
  filename: string;
  file_type: string;
  size_bytes: number;
  location: string;
  uploaded_at: string;
}

export interface DocumentListResponse {
  total_documents: number;
  documents: UploadedDocument[];
}

export interface UploadResponse {
  document_id: string;
  filename: string;
  file_type: string;
  size_bytes: number;
  chunks_indexed: number;
  message: string;
}

export interface ChatResponse {
  question: string;
  answer: string;
}

// In `ng serve` (development) call the local FastAPI server.
// In the production build (inside Docker) use the same address as the page.
const API_BASE = isDevMode() ? 'http://127.0.0.1:8000' : '';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private http = inject(HttpClient);

  private apiUrl = `${API_BASE}/api/documents`;
  private chatUrl = `${API_BASE}/api/chat`;

  getDocuments(): Observable<DocumentListResponse> {
    return this.http.get<DocumentListResponse>(this.apiUrl);
  }

  uploadDocument(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<UploadResponse>(
      `${this.apiUrl}/upload`,
      formData
    );
  }

  askQuestion(question: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(
      this.chatUrl,
      { question }
    );
  }
}