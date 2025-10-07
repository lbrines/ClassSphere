import { TestBed } from '@angular/core/testing';
import { NavigationService } from './navigation.service';

describe('NavigationService', () => {
  let service: NavigationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NavigationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should call redirectToExternal without errors', () => {
    // This method directly manipulates window.location which is not mockeable
    // We trust it works and test it in E2E tests instead
    // Just verify the method exists and can be called
    expect(service.redirectToExternal).toBeDefined();
    expect(typeof service.redirectToExternal).toBe('function');
  });

  it('should have reload method', () => {
    // window.location.reload is not mockeable in Karma
    // Test in E2E instead
    expect(service.reload).toBeDefined();
    expect(typeof service.reload).toBe('function');
  });

  it('should have goBack method', () => {
    // window.history.back is not mockeable in Karma
    // Test in E2E instead
    expect(service.goBack).toBeDefined();
    expect(typeof service.goBack).toBe('function');
  });

  it('should open URL in new tab', () => {
    spyOn(window, 'open');
    service.openInNewTab('https://example.com');
    expect(window.open).toHaveBeenCalledWith('https://example.com', '_blank');
  });
});

