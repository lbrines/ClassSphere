import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BehaviorSubject } from 'rxjs';

import { NotificationBadgeComponent } from './notification-badge.component';
import { NotificationService } from '../../../../core/services/notification.service';

describe('NotificationBadgeComponent', () => {
  let component: NotificationBadgeComponent;
  let fixture: ComponentFixture<NotificationBadgeComponent>;
  let notificationService: jasmine.SpyObj<NotificationService>;
  let unreadCountSubject: BehaviorSubject<number>;

  beforeEach(async () => {
    unreadCountSubject = new BehaviorSubject<number>(3);

    const notificationServiceSpy = jasmine.createSpyObj('NotificationService', [], {
      unreadCount$: unreadCountSubject.asObservable(),
    });

    await TestBed.configureTestingModule({
      imports: [NotificationBadgeComponent],
      providers: [{ provide: NotificationService, useValue: notificationServiceSpy }],
    }).compileComponents();

    fixture = TestBed.createComponent(NotificationBadgeComponent);
    component = fixture.componentInstance;
    notificationService = TestBed.inject(
      NotificationService
    ) as jasmine.SpyObj<NotificationService>;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display unread count', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const badge = compiled.querySelector('.badge-count');

    expect(badge?.textContent).toContain('3');
  });

  it('should hide badge when count is 0', () => {
    unreadCountSubject.next(0);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const badge = compiled.querySelector('.badge-count');

    expect(badge).toBeFalsy();
  });

  it('should show "9+" for counts greater than 9', () => {
    unreadCountSubject.next(15);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const badge = compiled.querySelector('.badge-count');

    expect(badge?.textContent).toContain('9+');
  });

  it('should emit click event when clicked', () => {
    spyOn(component.badgeClicked, 'emit');
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const badge = compiled.querySelector('.notification-badge') as HTMLElement;
    badge.click();

    expect(component.badgeClicked.emit).toHaveBeenCalled();
  });

  it('should have proper accessibility attributes', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const badge = compiled.querySelector('.notification-badge');

    expect(badge?.getAttribute('role')).toBe('button');
    expect(badge?.getAttribute('aria-label')?.toLowerCase()).toContain('notification');
  });
});
