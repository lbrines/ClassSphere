import { Injectable } from '@angular/core';

/**
 * Service to handle browser navigation operations.
 * Abstraction allows for better testability of window.location manipulations.
 */
@Injectable({ providedIn: 'root' })
export class NavigationService {
  /**
   * Redirects the browser to an external URL.
   * This triggers a full page reload and navigation.
   * 
   * @param url - The external URL to navigate to
   */
  redirectToExternal(url: string): void {
    window.location.href = url;
  }

  /**
   * Reloads the current page.
   */
  reload(): void {
    window.location.reload();
  }

  /**
   * Navigates back in browser history.
   */
  goBack(): void {
    window.history.back();
  }

  /**
   * Opens URL in a new tab.
   * 
   * @param url - The URL to open
   */
  openInNewTab(url: string): void {
    window.open(url, '_blank');
  }
}

