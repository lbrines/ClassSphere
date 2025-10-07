import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CoordinatorDashboardComponent } from './coordinator-dashboard.component';

describe('CoordinatorDashboardComponent', () => {
  let component: CoordinatorDashboardComponent;
  let fixture: ComponentFixture<CoordinatorDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CoordinatorDashboardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(CoordinatorDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render coordinator dashboard title', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h2')?.textContent).toContain('Coordinator Console');
  });

  it('should render coordinator description', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('p')?.textContent).toContain('Manage course allocations');
  });
});

