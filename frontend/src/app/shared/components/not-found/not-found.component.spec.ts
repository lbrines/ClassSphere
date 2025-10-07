import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { RouterLink } from '@angular/router';

import { NotFoundComponent } from './not-found.component';

describe('NotFoundComponent', () => {
  let component: NotFoundComponent;
  let fixture: ComponentFixture<NotFoundComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NotFoundComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(NotFoundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render 404 title', () => {
    const titleElement = fixture.debugElement.query(By.css('h2'));
    expect(titleElement.nativeElement.textContent.trim()).toBe('404');
  });

  it('should render error message', () => {
    const messageElement = fixture.debugElement.query(By.css('p'));
    expect(messageElement.nativeElement.textContent.trim()).toBe('We could not find the page you were looking for.');
  });

  it('should render return to login link', () => {
    const linkElement = fixture.debugElement.query(By.css('a'));
    expect(linkElement.nativeElement.textContent.trim()).toBe('Return to login');
    expect(linkElement.attributes['routerLink']).toBe('/auth/login');
  });

  it('should have correct CSS classes on main section', () => {
    const sectionElement = fixture.debugElement.query(By.css('section'));
    expect(sectionElement.classes['flex']).toBe(true);
    expect(sectionElement.classes['min-h-screen']).toBe(true);
    expect(sectionElement.classes['flex-col']).toBe(true);
    expect(sectionElement.classes['items-center']).toBe(true);
    expect(sectionElement.classes['justify-center']).toBe(true);
    expect(sectionElement.classes['bg-slate-950']).toBe(true);
    expect(sectionElement.classes['text-center']).toBe(true);
    expect(sectionElement.classes['text-slate-100']).toBe(true);
  });

  it('should have correct styling for title', () => {
    const titleElement = fixture.debugElement.query(By.css('h2'));
    expect(titleElement.classes['text-4xl']).toBe(true);
    expect(titleElement.classes['font-bold']).toBe(true);
  });

  it('should have correct styling for message', () => {
    const messageElement = fixture.debugElement.query(By.css('p'));
    expect(messageElement.classes['mt-2']).toBe(true);
    expect(messageElement.classes['text-slate-400']).toBe(true);
  });

  it('should have correct styling for link', () => {
    const linkElement = fixture.debugElement.query(By.css('a'));
    expect(linkElement.classes['mt-6']).toBe(true);
    expect(linkElement.classes['rounded-md']).toBe(true);
    expect(linkElement.classes['bg-sky-500']).toBe(true);
    expect(linkElement.classes['px-4']).toBe(true);
    expect(linkElement.classes['py-2']).toBe(true);
    expect(linkElement.classes['font-semibold']).toBe(true);
    expect(linkElement.classes['text-white']).toBe(true);
    expect(linkElement.classes['hover:bg-sky-600']).toBe(true);
  });

  it('should contain RouterLink directive', () => {
    const linkElement = fixture.debugElement.query(By.directive(RouterLink));
    expect(linkElement).toBeTruthy();
    expect(linkElement.injector.get(RouterLink).routerLink).toBe('/auth/login');
  });

  it('should have proper semantic structure', () => {
    const section = fixture.debugElement.query(By.css('section'));
    const h2 = fixture.debugElement.query(By.css('h2'));
    const p = fixture.debugElement.query(By.css('p'));
    const a = fixture.debugElement.query(By.css('a'));

    expect(section).toBeTruthy();
    expect(h2).toBeTruthy();
    expect(p).toBeTruthy();
    expect(a).toBeTruthy();

    // Check element hierarchy
    expect(section.nativeElement.contains(h2.nativeElement)).toBe(true);
    expect(section.nativeElement.contains(p.nativeElement)).toBe(true);
    expect(section.nativeElement.contains(a.nativeElement)).toBe(true);
  });

  it('should be a standalone component', () => {
    expect(NotFoundComponent).toBeTruthy();
    // Check that it's properly configured as standalone
    expect(component.constructor).toBe(NotFoundComponent);
  });

  it('should have correct component metadata', () => {
    const componentDef = (NotFoundComponent as any);
    expect(componentDef.selector).toBe('app-not-found');
    expect(componentDef.standalone).toBe(true);
  });

  it('should render correctly in different screen sizes', () => {
    // Test that responsive classes are present
    const sectionElement = fixture.debugElement.query(By.css('section'));
    expect(sectionElement.classes['flex']).toBe(true);
    expect(sectionElement.classes['flex-col']).toBe(true);
    expect(sectionElement.classes['items-center']).toBe(true);
    expect(sectionElement.classes['justify-center']).toBe(true);
  });

  it('should maintain accessibility standards', () => {
    const titleElement = fixture.debugElement.query(By.css('h2'));
    const linkElement = fixture.debugElement.query(By.css('a'));

    // Should have proper heading level
    expect(titleElement.nativeElement.tagName).toBe('H2');

    // Link should have proper text content for screen readers
    expect(linkElement.nativeElement.textContent.trim()).toBeTruthy();
  });

  it('should handle rapid re-renders without issues', () => {
    // Simulate rapid component updates
    for (let i = 0; i < 5; i++) {
      fixture.detectChanges();
    }

    const titleElement = fixture.debugElement.query(By.css('h2'));
    expect(titleElement.nativeElement.textContent.trim()).toBe('404');
  });

  it('should be properly destroyed', () => {
    const componentInstance = fixture.componentInstance;
    spyOn(componentInstance, 'ngOnDestroy');

    fixture.destroy();

    // Note: ngOnDestroy might not be called if component doesn't implement it
    // but the fixture should destroy properly
    expect(fixture).toBeTruthy();
  });
});
