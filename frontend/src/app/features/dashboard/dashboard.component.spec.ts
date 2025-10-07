import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { of, BehaviorSubject } from 'rxjs';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { DashboardComponent } from './dashboard.component';
import { AuthService } from '../../core/services/auth.service';
import { UserRole, User } from '../../core/models/user.model';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;
  let mockAuthService: jasmine.SpyObj<AuthService>;
  let mockRouter: jasmine.SpyObj<Router>;
  let currentUserSubject: BehaviorSubject<User | null>;

  beforeEach(async () => {
    currentUserSubject = new BehaviorSubject<User | null>({ 
      id: '1', 
      email: 'test@test.com', 
      role: 'teacher' as UserRole, 
      displayName: 'Test User'
    });

    const authServiceSpy = jasmine.createSpyObj('AuthService', [], {
      currentUser$: currentUserSubject.asObservable()
    });
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [DashboardComponent, HttpClientTestingModule],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    mockAuthService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    mockRouter = TestBed.inject(Router) as jasmine.SpyObj<Router>;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set role from current user', () => {
    fixture.detectChanges();
    expect(component.role).toBe('teacher');
  });

  it('should redirect to login if no user', () => {
    currentUserSubject.next(null);
    fixture.detectChanges();
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/auth/login']);
  });

  it('should show admin dashboard for admin role', () => {
    currentUserSubject.next({ 
      id: '1', 
      email: 'admin@test.com', 
      role: 'admin' as UserRole, 
      displayName: 'Admin'
    });
    fixture.detectChanges();
    expect(component.role).toBe('admin');
  });

  it('should show coordinator dashboard for coordinator role', () => {
    currentUserSubject.next({ 
      id: '1', 
      email: 'coord@test.com', 
      role: 'coordinator' as UserRole, 
      displayName: 'Coordinator'
    });
    fixture.detectChanges();
    expect(component.role).toBe('coordinator');
  });

  it('should show student dashboard for student role', () => {
    currentUserSubject.next({ 
      id: '1', 
      email: 'student@test.com', 
      role: 'student' as UserRole, 
      displayName: 'Student'
    });
    fixture.detectChanges();
    expect(component.role).toBe('student');
  });
});