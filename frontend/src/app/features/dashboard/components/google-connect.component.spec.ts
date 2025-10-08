import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { BehaviorSubject, Subject, of, throwError } from 'rxjs';

import { ClassroomService } from '../../../core/services/classroom.service';
import { AuthService } from '../../../core/services/auth.service';
import { GoogleConnectComponent } from './google-connect.component';

describe('GoogleConnectComponent', () => {
  let fixture: ComponentFixture<GoogleConnectComponent>;
  let authService: jasmine.SpyObj<AuthService>;
  let classroomService: jasmine.SpyObj<ClassroomService>;
  let modeSubject: BehaviorSubject<'mock' | 'google'>;
  let openSpy: jasmine.Spy<(url?: string, target?: string) => Window | null>;

  beforeEach(async () => {
    modeSubject = new BehaviorSubject<'mock' | 'google'>('mock');
    authService = jasmine.createSpyObj<AuthService>('AuthService', ['startOAuth']);
    classroomService = jasmine.createSpyObj<ClassroomService>('ClassroomService', [], {
      mode$: modeSubject.asObservable(),
    });

    authService.startOAuth.and.returnValue(of({ state: 'state', url: 'https://accounts.google.com' }));

    await TestBed.configureTestingModule({
      imports: [GoogleConnectComponent],
      providers: [
        { provide: ClassroomService, useValue: classroomService },
        { provide: AuthService, useValue: authService },
      ],
    }).compileComponents();

    openSpy = spyOn(window, 'open').and.returnValue(null);
    fixture = TestBed.createComponent(GoogleConnectComponent);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('should display mock mode message when mode is mock', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const mockElement = compiled.querySelector('h3');
    expect(mockElement?.textContent?.trim()).toBe('Mock data active');
  });

  it('should display google mode message when mode is google', () => {
    modeSubject.next('google');
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const googleElement = compiled.querySelector('h3');
    expect(googleElement?.textContent).toContain('Connected');
  });

  it('should initiate OAuth flow on connect', () => {
    openSpy.calls.reset();
    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));
    expect(authService.startOAuth).toHaveBeenCalled();
    expect(openSpy).toHaveBeenCalledWith('https://accounts.google.com', '_self');
  });

  it('should not initiate OAuth when already connecting', () => {
    const component = fixture.componentInstance;
    component.connecting = true;

    openSpy.calls.reset();
    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));

    expect(authService.startOAuth).not.toHaveBeenCalled();
    expect(openSpy).not.toHaveBeenCalled();
  });

  it('should show loading state when connecting', () => {
    const component = fixture.componentInstance;
    component.connecting = true;
    fixture.detectChanges();

    const button = fixture.debugElement.query(By.css('button'));
    expect(button.nativeElement.textContent).toContain('Redirecting…');
    expect(button.nativeElement.disabled).toBe(true);
  });

  it('should show success message when OAuth succeeds', () => {
    const component = fixture.componentInstance;
    component.connecting = true;
    component.success = true;
    component.message = 'Redirecting to Google…';
    fixture.detectChanges();

    const message = fixture.debugElement.query(By.css('span.text-sm'));
    expect(message.nativeElement.textContent).toContain('Redirecting to Google…');
    expect(message.classes['text-emerald-300']).toBe(true);
  });

  it('should show error message when OAuth fails', () => {
    authService.startOAuth.and.returnValue(throwError(() => new Error('OAuth failure')));
    fixture.detectChanges();

    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));
    fixture.detectChanges();

    const message = fixture.debugElement.query(By.css('span.text-sm'));
    expect(message.nativeElement.textContent).toContain('Failed to start Google authentication');
    expect(message.classes['text-rose-300']).toBe(true);
  });

  it('should handle multiple rapid clicks gracefully', () => {
    const oauthSubject = new Subject<{ state: string; url: string }>();
    authService.startOAuth.and.returnValue(oauthSubject.asObservable());

    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));
    button.triggerEventHandler('click', new Event('click'));

    expect(authService.startOAuth).toHaveBeenCalledTimes(1);

    oauthSubject.next({ state: 'state', url: 'https://accounts.google.com' });
    oauthSubject.complete();
  });

  it('should handle OAuth with different URLs', () => {
    authService.startOAuth.and.returnValue(of({ state: 'state123', url: 'https://custom-oauth.example.com' }));
    openSpy.calls.reset();

    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));

    expect(openSpy).toHaveBeenCalledWith('https://custom-oauth.example.com', '_self');
  });

  it('should store OAuth state in sessionStorage', () => {
    const setItemSpy = spyOn(sessionStorage, 'setItem');

    const button = fixture.debugElement.query(By.css('button'));
    button.triggerEventHandler('click', new Event('click'));

    expect(setItemSpy).toHaveBeenCalledWith('classsphere.oauth.state', 'state');
  });
});
