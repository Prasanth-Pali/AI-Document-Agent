import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { DashboardComponent } from './dashboard.component';
import { DocumentService } from '../../services/document.service';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardComponent],
      providers: [{
        provide: DocumentService,
        useValue: {
          getDocuments: () => of({ total_documents: 0, documents: [] })
        }
      }]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
