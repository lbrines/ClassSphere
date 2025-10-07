import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { of, throwError } from 'rxjs';

import { ClassroomService } from '../../../core/services/classroom.service';
import { AuthService } from '../../../core/services/auth.service';
import { GoogleConnectComponent } from './google-connect.component';

class ClassroomServiceStub {
  readonly mode$ = of<'mock'>('mock');
}

describe('GoogleConnectComponent', () => {
  let fixture: ComponentFixture<GoogleConnectComponent>;
  let authService: jasmine.SpyObj<AuthService>;

  beforeEach(async () => {
    authService = jasmine.createSpyObj<AuthService>('AuthService', ['startOAuth']);
    authService.startOAuth.and.returnValue(of({ state: 'state', url: 'https://accounts.google.com' }));

    await TestBed.configureTestingModule({
      imports: [GoogleConnectComponent],
      providers: [
        { provide: ClassroomService, useClass: ClassroomServiceStub },
        { provide: AuthService, useValue: authService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(GoogleConnectComponent);
    fixture.detectChanges();
  });

  it('initiates OAuth flow on connect', () => {
    const openSpy = spyOn(window, 'open');
    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));
    expect(authService.startOAuth).toHaveBeenCalled();
    expect(openSpy).toHaveBeenCalledWith('https://accounts.google.com', '_self');
  });

  it('shows error message when OAuth fails', () => {
    authService.startOAuth.and.returnValue(throwError(() => new Error('failure')));
    fixture.detectChanges();

    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));
    fixture.detectChanges();

    const message = fixture.debugElement.query(By.css('span.text-sm'));
    expect(message.nativeElement.textContent).toContain('Failed to start Google authentication');
  });
});
