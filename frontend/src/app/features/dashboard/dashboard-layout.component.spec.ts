import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';

import { DashboardLayoutComponent } from './dashboard-layout.component';
import { AuthService } from '../../core/services/auth.service';
import { ClassroomService } from '../../core/services/classroom.service';
import { IntegrationMode } from '../../core/models/classroom.model';
import { User, UserRole } from '../../core/models/user.model';

class ClassroomServiceStub {
  readonly mode$ = of<IntegrationMode>('mock');
  readonly courseState$ = of({
    mode: 'mock' as IntegrationMode,
    generatedAt: '2025-10-07T10:00:00Z',
    availableModes: ['mock'] as IntegrationMode[],
    courses: [],
  });
  readonly availableModes$ = of(['mock'] as IntegrationMode[]);
  setMode = jasmine.createSpy('setMode');
  refresh = jasmine.createSpy('refresh');
}

describe('DashboardLayoutComponent', () => {
  let component: DashboardLayoutComponent;
  let fixture: ComponentFixture<DashboardLayoutComponent>;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  const mockUser: User = {
    id: 'user-1',
    email: 'test@example.com',
    displayName: 'Test User',
    role: 'admin' as UserRole,
  };

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('AuthService', ['logout'], {
      currentUser$: of(mockUser),
    });

    await TestBed.configureTestingModule({
      imports: [DashboardLayoutComponent, RouterTestingModule],
      providers: [
        { provide: AuthService, useValue: spy },
        { provide: ClassroomService, useClass: ClassroomServiceStub },
      ],
    }).compileComponents();

    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    fixture = TestBed.createComponent(DashboardLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render ClassSphere title', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('ClassSphere');
  });

  it('should display user information', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Test User');
    expect(compiled.textContent).toContain('Admin');
  });

  it('should have router outlet', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('router-outlet')).toBeTruthy();
  });
});
