
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DocumentService, UploadedDocument } from '../../services/document.service';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {

  

  private documentService = inject(DocumentService);
  

  documents: UploadedDocument[] = [];
  isUploading = false;
  isLoading = false;
  successMessage = '';
  errorMessage = '';
  question = '';
  answer = '';
  isChatLoading = false;
  chatError = '';

  ngOnInit(): void {
    this.loadDocuments();
  }

  loadDocuments(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.documentService.getDocuments().subscribe({
      next: (response) => {
        this.documents = response.documents;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Failed to load documents:', error);
        this.errorMessage = 'Unable to load documents. Check whether FastAPI is running.';
        this.isLoading = false;
      }
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) {
      return;
    }

    const allowedExtensions = ['.pdf', '.docx', '.csv', '.txt'];
    const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      this.errorMessage = 'Only PDF, DOCX, CSV and TXT files are supported.';
      input.value = '';
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      this.errorMessage = 'File size must not exceed 10 MB.';
      input.value = '';
      return;
    }

    this.isUploading = true;
    this.successMessage = '';
    this.errorMessage = '';

    this.documentService.uploadDocument(file).subscribe({
      next: (response) => {
        this.successMessage =
          `${response.filename} uploaded and indexed successfully.`;

        this.isUploading = false;
        input.value = '';
        this.loadDocuments();

        // Automatically hide the success message after 3 seconds
        setTimeout(() => {
          this.successMessage = '';
          }, 3000);
      },
      error: (error) => {
        console.error('Upload failed:', error);

        this.errorMessage =
          error.error?.detail ?? 'Upload failed. Please try again.';

        this.isUploading = false;
        input.value = '';
      }
    });
  }
askAI(): void {
  const question = this.question.trim();

  if (!question || this.isChatLoading) {
    return;
  }

  this.isChatLoading = true;
  this.answer = '';
  this.chatError = '';

  // Clear the input box after capturing the question
  this.question = '';

  this.documentService.askQuestion(question).subscribe({
    next: (response) => {
      this.answer = response.answer;
      this.isChatLoading = false;
    },
    error: (error) => {
      console.error('AI chat failed:', error);

      this.chatError =
        error.error?.detail ??
        'Unable to get an answer. Please check the backend and try again.';

      this.isChatLoading = false;
    }
  });
}
}
