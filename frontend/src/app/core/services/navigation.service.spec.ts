import { TestBed } from '@angular/core/testing';
import { NavigationService } from './navigation.service';

describe('NavigationService', () => {
  let service: NavigationService;

  // Mock window.location for testing
  let mockLocation: jasmine.SpyObj<Location>;
  let mockHistory: jasmine.SpyObj<History>;

  beforeEach(() => {
    // Create mocks for window.location and window.history
    mockLocation = jasmine.createSpyObj('Location', ['assign'], {
      href: 'http://localhost:4200'
    });
    mockHistory = jasmine.createSpyObj('History', ['back']);

    // Mock window object
    Object.defineProperty(window, 'location', {
      value: mockLocation,
      writable: true
    });
    Object.defineProperty(window, 'history', {
      value: mockHistory,
      writable: true
    });

    TestBed.configureTestingModule({});
    service = TestBed.inject(NavigationService);
  });

  afterEach(() => {
    // Reset window.location after each test
    Object.defineProperty(window, 'location', {
      value: { href: 'http://localhost:4200' },
      writable: true
    });
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('redirectToExternal', () => {
    it('should set window.location.href to redirect to external URL', () => {
      const testUrl = 'https://google.com';
      service.redirectToExternal(testUrl);
      expect(mockLocation.href).toBe(testUrl);
    });

    it('should handle empty string URL', () => {
      service.redirectToExternal('');
      expect(mockLocation.href).toBe('');
    });

    it('should handle URL with special characters', () => {
      const specialUrl = 'https://example.com/path?param=value&other=test';
      service.redirectToExternal(specialUrl);
      expect(mockLocation.href).toBe(specialUrl);
    });

    it('should handle relative URLs', () => {
      const relativeUrl = '/dashboard';
      service.redirectToExternal(relativeUrl);
      expect(mockLocation.href).toBe(relativeUrl);
    });

    it('should handle URLs with fragments', () => {
      const fragmentUrl = 'https://example.com#section';
      service.redirectToExternal(fragmentUrl);
      expect(mockLocation.href).toBe(fragmentUrl);
    });

    it('should handle long URLs', () => {
      const longUrl = 'https://example.com/very/long/path/with/many/segments/and/parameters?param1=value1&param2=value2&param3=value3&param4=value4&param5=value5';
      service.redirectToExternal(longUrl);
      expect(mockLocation.href).toBe(longUrl);
    });
  });

  describe('reload', () => {
    it('should call window.location.reload', () => {
      spyOn(window.location, 'reload');
      service.reload();
      expect(window.location.reload).toHaveBeenCalled();
    });

    it('should handle reload when window.location is not available', () => {
      // Temporarily remove location.reload
      const originalReload = window.location.reload;
      delete (window.location as any).reload;

      // Should not throw error
      expect(() => service.reload()).not.toThrow();

      // Restore
      window.location.reload = originalReload;
    });
  });

  describe('goBack', () => {
    it('should call window.history.back', () => {
      service.goBack();
      expect(mockHistory.back).toHaveBeenCalled();
    });

    it('should handle goBack when history is not available', () => {
      // Temporarily remove history
      const originalHistory = window.history;
      delete (window as any).history;

      // Should not throw error
      expect(() => service.goBack()).not.toThrow();

      // Restore
      window.history = originalHistory;
    });
  });

  describe('openInNewTab', () => {
    it('should open URL in new tab with _blank target', () => {
      spyOn(window, 'open');
      const testUrl = 'https://example.com';
      service.openInNewTab(testUrl);
      expect(window.open).toHaveBeenCalledWith(testUrl, '_blank');
    });

    it('should handle empty string URL', () => {
      spyOn(window, 'open');
      service.openInNewTab('');
      expect(window.open).toHaveBeenCalledWith('', '_blank');
    });

    it('should handle URL with special characters', () => {
      spyOn(window, 'open');
      const specialUrl = 'https://example.com/path?param=value&other=test';
      service.openInNewTab(specialUrl);
      expect(window.open).toHaveBeenCalledWith(specialUrl, '_blank');
    });

    it('should handle relative URLs', () => {
      spyOn(window, 'open');
      const relativeUrl = '/dashboard';
      service.openInNewTab(relativeUrl);
      expect(window.open).toHaveBeenCalledWith(relativeUrl, '_blank');
    });

    it('should handle URLs with fragments', () => {
      spyOn(window, 'open');
      const fragmentUrl = 'https://example.com#section';
      service.openInNewTab(fragmentUrl);
      expect(window.open).toHaveBeenCalledWith(fragmentUrl, '_blank');
    });

    it('should handle when window.open returns null', () => {
      spyOn(window, 'open').and.returnValue(null);
      const testUrl = 'https://example.com';
      service.openInNewTab(testUrl);
      expect(window.open).toHaveBeenCalledWith(testUrl, '_blank');
    });

    it('should handle when window.open throws error', () => {
      spyOn(window, 'open').and.throwError('Popup blocked');
      const testUrl = 'https://example.com';
      // Should not throw error
      expect(() => service.openInNewTab(testUrl)).not.toThrow();
    });
  });

  describe('integration tests', () => {
    it('should handle multiple consecutive calls', () => {
      spyOn(window, 'open');

      service.openInNewTab('https://example1.com');
      service.openInNewTab('https://example2.com');
      service.openInNewTab('https://example3.com');

      expect(window.open).toHaveBeenCalledTimes(3);
      expect(window.open).toHaveBeenCalledWith('https://example1.com', '_blank');
      expect(window.open).toHaveBeenCalledWith('https://example2.com', '_blank');
      expect(window.open).toHaveBeenCalledWith('https://example3.com', '_blank');
    });

    it('should handle different URL protocols', () => {
      spyOn(window, 'open');

      service.openInNewTab('https://secure.com');
      service.openInNewTab('http://insecure.com');
      service.openInNewTab('ftp://files.com');

      expect(window.open).toHaveBeenCalledTimes(3);
    });

    it('should handle international URLs', () => {
      spyOn(window, 'open');
      const internationalUrl = 'https://example.中国';
      service.openInNewTab(internationalUrl);
      expect(window.open).toHaveBeenCalledWith(internationalUrl, '_blank');
    });
  });

  describe('error handling', () => {
    it('should handle window.location being read-only', () => {
      // Make location.href read-only
      Object.defineProperty(window.location, 'href', {
        value: 'http://readonly.com',
        writable: false,
        configurable: true
      });

      // Should not throw error
      expect(() => service.redirectToExternal('https://example.com')).not.toThrow();

      // Restore
      Object.defineProperty(window.location, 'href', {
        value: 'http://localhost:4200',
        writable: true,
        configurable: true
      });
    });

    it('should handle window object being partially undefined', () => {
      // Temporarily remove location
      const originalLocation = window.location;
      delete (window as any).location;

      // Should not throw error for methods that don't use location
      expect(() => service.goBack()).not.toThrow();

      // Restore
      window.location = originalLocation;
    });
  });
});

