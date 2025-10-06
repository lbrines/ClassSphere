import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, fromEvent, merge } from 'rxjs';
import { map, distinctUntilChanged } from 'rxjs/operators';

export interface PWAInstallPrompt {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export interface PWAUpdateInfo {
  available: boolean;
  currentVersion: string;
  newVersion: string;
  releaseNotes?: string;
}

export interface PWANetworkStatus {
  online: boolean;
  connectionType: string;
  effectiveType: string;
  downlink: number;
  rtt: number;
}

@Injectable({
  providedIn: 'root'
})
export class PwaService {
  private installPromptSubject = new BehaviorSubject<PWAInstallPrompt | null>(null);
  private updateInfoSubject = new BehaviorSubject<PWAUpdateInfo | null>(null);
  private networkStatusSubject = new BehaviorSubject<PWANetworkStatus>({
    online: navigator.onLine,
    connectionType: 'unknown',
    effectiveType: 'unknown',
    downlink: 0,
    rtt: 0
  });
  private swRegistration: ServiceWorkerRegistration | null = null;

  constructor() {
    this.initializePWA();
    this.monitorNetworkStatus();
    this.monitorServiceWorker();
  }

  // Install Prompt
  get installPrompt$(): Observable<PWAInstallPrompt | null> {
    return this.installPromptSubject.asObservable();
  }

  // Update Info
  get updateInfo$(): Observable<PWAUpdateInfo | null> {
    return this.updateInfoSubject.asObservable();
  }

  // Network Status
  get networkStatus$(): Observable<PWANetworkStatus> {
    return this.networkStatusSubject.asObservable();
  }

  // Online Status
  get isOnline$(): Observable<boolean> {
    return this.networkStatus$.pipe(
      map(status => status.online),
      distinctUntilChanged()
    );
  }

  private initializePWA(): void {
    // Register service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/service-worker.js')
        .then(registration => {
          console.log('[PWA] Service Worker registered:', registration);
          this.swRegistration = registration;
          this.checkForUpdates();
        })
        .catch(error => {
          console.error('[PWA] Service Worker registration failed:', error);
        });
    }

    // Listen for install prompt
    window.addEventListener('beforeinstallprompt', (event: any) => {
      console.log('[PWA] Install prompt triggered');
      event.preventDefault();
      
      const installPrompt: PWAInstallPrompt = {
        prompt: () => event.prompt(),
        userChoice: event.userChoice
      };
      
      this.installPromptSubject.next(installPrompt);
    });

    // Listen for app installed
    window.addEventListener('appinstalled', () => {
      console.log('[PWA] App installed successfully');
      this.installPromptSubject.next(null);
    });

    // Listen for PWA display mode changes
    this.monitorDisplayMode();
  }

  private monitorDisplayMode(): void {
    const displayMode = window.matchMedia('(display-mode: standalone)').matches;
    console.log('[PWA] Display mode:', displayMode ? 'standalone' : 'browser');

    // Listen for display mode changes
    window.matchMedia('(display-mode: standalone)').addEventListener('change', (e) => {
      console.log('[PWA] Display mode changed:', e.matches ? 'standalone' : 'browser');
    });
  }

  private monitorNetworkStatus(): void {
    // Listen for online/offline events
    const online$ = fromEvent(window, 'online').pipe(map(() => true));
    const offline$ = fromEvent(window, 'offline').pipe(map(() => false));
    
    merge(online$, offline$).subscribe(online => {
      const currentStatus = this.networkStatusSubject.value;
      this.networkStatusSubject.next({
        ...currentStatus,
        online
      });
    });

    // Monitor connection information
    if ('connection' in navigator) {
      const connection = (navigator as any).connection;
      
      const updateConnectionInfo = () => {
        const currentStatus = this.networkStatusSubject.value;
        this.networkStatusSubject.next({
          ...currentStatus,
          connectionType: connection.type || 'unknown',
          effectiveType: connection.effectiveType || 'unknown',
          downlink: connection.downlink || 0,
          rtt: connection.rtt || 0
        });
      };

      connection.addEventListener('change', updateConnectionInfo);
      updateConnectionInfo();
    }
  }

  private monitorServiceWorker(): void {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        console.log('[PWA] Service Worker controller changed');
        this.checkForUpdates();
      });

      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'SW_UPDATE_AVAILABLE') {
          this.updateInfoSubject.next({
            available: true,
            currentVersion: event.data.currentVersion,
            newVersion: event.data.newVersion,
            releaseNotes: event.data.releaseNotes
          });
        }
      });
    }
  }

  private checkForUpdates(): void {
    if (this.swRegistration) {
      this.swRegistration.update().then(() => {
        console.log('[PWA] Service Worker update check completed');
      }).catch(error => {
        console.error('[PWA] Service Worker update check failed:', error);
      });
    }
  }

  // Public methods
  async installApp(): Promise<boolean> {
    const installPrompt = this.installPromptSubject.value;
    if (!installPrompt) {
      return false;
    }

    try {
      await installPrompt.prompt();
      const choiceResult = await installPrompt.userChoice;
      
      if (choiceResult.outcome === 'accepted') {
        console.log('[PWA] User accepted install prompt');
        this.installPromptSubject.next(null);
        return true;
      } else {
        console.log('[PWA] User dismissed install prompt');
        return false;
      }
    } catch (error) {
      console.error('[PWA] Install prompt failed:', error);
      return false;
    }
  }

  async updateApp(): Promise<boolean> {
    if (!this.swRegistration) {
      return false;
    }

    try {
      const registration = await this.swRegistration.update();
      
      if (registration.waiting) {
        // Send skip waiting message to service worker
        registration.waiting.postMessage({ type: 'SKIP_WAITING' });
        
        // Reload the page to activate the new service worker
        window.location.reload();
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('[PWA] App update failed:', error);
      return false;
    }
  }

  async getAppInfo(): Promise<any> {
    const manifest = await fetch('/manifest.json').then(response => response.json());
    
    return {
      name: manifest.name,
      shortName: manifest.short_name,
      version: manifest.version || '1.0.0',
      description: manifest.description,
      themeColor: manifest.theme_color,
      backgroundColor: manifest.background_color,
      displayMode: window.matchMedia('(display-mode: standalone)').matches ? 'standalone' : 'browser',
      isInstalled: window.matchMedia('(display-mode: standalone)').matches,
      installable: this.installPromptSubject.value !== null
    };
  }

  async clearCache(): Promise<void> {
    if ('caches' in window) {
      const cacheNames = await caches.keys();
      await Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
      );
      console.log('[PWA] All caches cleared');
    }
  }

  async getCacheInfo(): Promise<any> {
    if (!('caches' in window)) {
      return null;
    }

    const cacheNames = await caches.keys();
    const cacheInfo = await Promise.all(
      cacheNames.map(async (cacheName) => {
        const cache = await caches.open(cacheName);
        const keys = await cache.keys();
        return {
          name: cacheName,
          size: keys.length,
          keys: keys.map(request => request.url)
        };
      })
    );

    return {
      totalCaches: cacheNames.length,
      caches: cacheInfo
    };
  }

  // Notification methods
  async requestNotificationPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      return 'denied';
    }

    if (Notification.permission === 'granted') {
      return 'granted';
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission();
      return permission;
    }

    return 'denied';
  }

  async showNotification(title: string, options?: NotificationOptions): Promise<void> {
    if (!this.swRegistration || Notification.permission !== 'granted') {
      return;
    }

    await this.swRegistration.showNotification(title, {
      icon: '/assets/icons/icon-192x192.png',
      badge: '/assets/icons/badge-72x72.png',
      ...options
    } as NotificationOptions);
  }

  // Background sync
  async registerBackgroundSync(tag: string): Promise<void> {
    if (!this.swRegistration || !('sync' in window.ServiceWorkerRegistration.prototype)) {
      return;
    }

    try {
      await (this.swRegistration as any).sync.register(tag);
      console.log('[PWA] Background sync registered:', tag);
    } catch (error) {
      console.error('[PWA] Background sync registration failed:', error);
    }
  }

  // Share API
  async share(data: ShareData): Promise<boolean> {
    if (!('share' in navigator)) {
      return false;
    }

    try {
      await navigator.share(data);
      return true;
    } catch (error) {
      console.error('[PWA] Share failed:', error);
      return false;
    }
  }

  // Device orientation
  getOrientation(): string {
    return screen.orientation?.type || 'unknown';
  }

  // Device capabilities
  getDeviceCapabilities(): any {
    return {
      touch: 'ontouchstart' in window,
      orientation: this.getOrientation(),
      standalone: window.matchMedia('(display-mode: standalone)').matches,
      share: 'share' in navigator,
      notifications: 'Notification' in window,
      serviceWorker: 'serviceWorker' in navigator,
      backgroundSync: 'sync' in window.ServiceWorkerRegistration.prototype,
      pushManager: 'PushManager' in window,
      geolocation: 'geolocation' in navigator,
      camera: 'mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices
    };
  }
}
