import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { RouterTestingModule } from '@angular/router/testing';

import { NotFoundComponent } from './not-found.component';

describe('NotFoundComponent', () => {
  let component: NotFoundComponent;
  let fixture: ComponentFixture<NotFoundComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NotFoundComponent, RouterTestingModule]
    }).compileComponents();

    fixture = TestBed.createComponent(NotFoundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the not found message', () => {
    const titleElement = fixture.debugElement.query(By.css('h2'));
    const messageElement = fixture.debugElement.query(By.css('p'));
    expect(titleElement.nativeElement.textContent.trim()).toBe('404');
    expect(messageElement.nativeElement.textContent.trim()).toContain('could not find');
  });

  it('should link back to the login page', () => {
    const linkDebug = fixture.debugElement.query(By.css('a'));
    expect(linkDebug.nativeElement.textContent.trim()).toBe('Return to login');
    expect(linkDebug.attributes['ng-reflect-router-link']).toBe('/auth/login');
  });
});
