import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TeacherDashboardComponent } from './teacher-dashboard.component';

describe('TeacherDashboardComponent', () => {
  let component: TeacherDashboardComponent;
  let fixture: ComponentFixture<TeacherDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeacherDashboardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(TeacherDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render teacher dashboard title', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h2')?.textContent).toContain('Teacher Workspace');
  });

  it('should render teacher description', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('p')?.textContent).toContain('Track classroom progress');
  });
});

