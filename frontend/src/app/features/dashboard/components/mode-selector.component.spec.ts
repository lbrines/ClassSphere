import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { BehaviorSubject, of } from 'rxjs';

import { IntegrationMode } from '../../../core/models/classroom.model';
import { ClassroomService } from '../../../core/services/classroom.service';
import { ModeSelectorComponent } from './mode-selector.component';

class ClassroomServiceStub {
  private readonly modeSubject = new BehaviorSubject<IntegrationMode>('mock');

  readonly mode$ = this.modeSubject.asObservable();
  readonly courseState$ = of({
    mode: 'mock' as IntegrationMode,
    generatedAt: '2025-10-07T10:00:00Z',
    availableModes: ['mock', 'google'] as IntegrationMode[],
    courses: [],
  });
  readonly availableModes$ = of(['mock', 'google'] as IntegrationMode[]);

  setMode = jasmine.createSpy('setMode');
  refresh = jasmine.createSpy('refresh');
}

describe('ModeSelectorComponent', () => {
  let fixture: ComponentFixture<ModeSelectorComponent>;
  let service: ClassroomServiceStub;

  beforeEach(async () => {
    service = new ClassroomServiceStub();

    await TestBed.configureTestingModule({
      imports: [ModeSelectorComponent],
      providers: [{ provide: ClassroomService, useValue: service }],
    }).compileComponents();

    fixture = TestBed.createComponent(ModeSelectorComponent);
    fixture.detectChanges();
  });

  it('renders available modes', () => {
    const labels = fixture.debugElement
      .queryAll(By.css('button'))
      .map((button) => button.nativeElement.textContent?.trim());
    expect(labels).toContain('Mock');
    expect(labels).toContain('Google');
  });

  it('delegates mode selection to service', () => {
    const googleButton = fixture.debugElement
      .queryAll(By.css('button'))
      .find((button) => button.nativeElement.textContent.includes('Google'));
    googleButton?.triggerEventHandler('click', new Event('click'));
    expect(service.setMode).toHaveBeenCalledWith('google');
  });

  it('refresh button triggers reload', () => {
    const refreshButton = fixture.debugElement
      .queryAll(By.css('button'))
      .find((button) => button.nativeElement.textContent.includes('Refresh'));
    refreshButton?.triggerEventHandler('click', new Event('click'));
    expect(service.refresh).toHaveBeenCalled();
  });
});
