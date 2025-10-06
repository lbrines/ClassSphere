import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface PerformanceMetrics {
  loadTime: number;
  renderTime: number;
  memoryUsage: number;
  bundleSize: number;
  cacheHitRate: number;
  apiResponseTime: number;
}

@Injectable({
  providedIn: 'root'
})
export class PerformanceService {
  private performanceMetrics$ = new BehaviorSubject<PerformanceMetrics>({
    loadTime: 0,
    renderTime: 0,
    memoryUsage: 0,
    bundleSize: 0,
    cacheHitRate: 0,
    apiResponseTime: 0
  });

  private startTimes = new Map<string, number>();
  private apiTimes = new Map<string, number[]>();

  constructor() {
    this.initializePerformanceMonitoring();
  }

  /**
   * Get performance metrics observable
   */
  getPerformanceMetrics(): Observable<PerformanceMetrics> {
    return this.performanceMetrics$.asObservable();
  }

  /**
   * Start timing a performance measurement
   */
  startTiming(label: string): void {
    this.startTimes.set(label, performance.now());
  }

  /**
   * End timing and record the measurement
   */
  endTiming(label: string): number {
    const startTime = this.startTimes.get(label);
    if (!startTime) {
      console.warn(`No start time found for label: ${label}`);
      return 0;
    }

    const duration = performance.now() - startTime;
    this.startTimes.delete(label);

    // Update specific metrics based on label
    this.updateMetrics(label, duration);

    return duration;
  }

  /**
   * Measure API response time
   */
  measureApiCall<T>(apiCall: () => Observable<T>, endpoint: string): Observable<T> {
    const startTime = performance.now();
    
    return apiCall().pipe(
      tap(() => {
        const duration = performance.now() - startTime;
        this.recordApiTime(endpoint, duration);
      })
    );
  }

  /**
   * Get current memory usage
   */
  getMemoryUsage(): number {
    if ('memory' in performance) {
      const memory = (performance as any).memory;
      return memory.usedJSHeapSize / 1024 / 1024; // MB
    }
    return 0;
  }

  /**
   * Get bundle size information
   */
  getBundleSize(): number {
    // This would typically come from build-time analysis
    // For now, we'll estimate based on known bundle sizes
    return 334.58; // KB from our build output
  }

  /**
   * Calculate cache hit rate
   */
  getCacheHitRate(): number {
    // This would be calculated based on cache service statistics
    // For now, we'll return a mock value
    return 0.85; // 85% hit rate
  }

  /**
   * Initialize performance monitoring
   */
  private initializePerformanceMonitoring(): void {
    // Monitor page load time
    window.addEventListener('load', () => {
      const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
      this.updateMetrics('pageLoad', loadTime);
    });

    // Monitor memory usage periodically
    setInterval(() => {
      const memoryUsage = this.getMemoryUsage();
      const currentMetrics = this.performanceMetrics$.value;
      this.performanceMetrics$.next({
        ...currentMetrics,
        memoryUsage
      });
    }, 30000); // Every 30 seconds

    // Monitor bundle size
    const bundleSize = this.getBundleSize();
    const currentMetrics = this.performanceMetrics$.value;
    this.performanceMetrics$.next({
      ...currentMetrics,
      bundleSize
    });
  }

  /**
   * Update specific metrics based on timing label
   */
  private updateMetrics(label: string, duration: number): void {
    const currentMetrics = this.performanceMetrics$.value;
    
    switch (label) {
      case 'pageLoad':
        this.performanceMetrics$.next({
          ...currentMetrics,
          loadTime: duration
        });
        break;
      case 'render':
        this.performanceMetrics$.next({
          ...currentMetrics,
          renderTime: duration
        });
        break;
      case 'apiCall':
        this.performanceMetrics$.next({
          ...currentMetrics,
          apiResponseTime: duration
        });
        break;
    }
  }

  /**
   * Record API response time for statistics
   */
  private recordApiTime(endpoint: string, duration: number): void {
    if (!this.apiTimes.has(endpoint)) {
      this.apiTimes.set(endpoint, []);
    }
    
    const times = this.apiTimes.get(endpoint)!;
    times.push(duration);
    
    // Keep only last 10 measurements
    if (times.length > 10) {
      times.shift();
    }
    
    // Update average API response time
    const averageTime = times.reduce((sum, time) => sum + time, 0) / times.length;
    const currentMetrics = this.performanceMetrics$.value;
    this.performanceMetrics$.next({
      ...currentMetrics,
      apiResponseTime: averageTime
    });
  }

  /**
   * Get performance report
   */
  getPerformanceReport(): {
    metrics: PerformanceMetrics;
    recommendations: string[];
  } {
    const metrics = this.performanceMetrics$.value;
    const recommendations: string[] = [];

    // Analyze performance and provide recommendations
    if (metrics.loadTime > 3000) {
      recommendations.push('Page load time is slow. Consider code splitting and lazy loading.');
    }

    if (metrics.renderTime > 100) {
      recommendations.push('Render time is high. Consider optimizing component rendering.');
    }

    if (metrics.memoryUsage > 50) {
      recommendations.push('Memory usage is high. Check for memory leaks.');
    }

    if (metrics.apiResponseTime > 1000) {
      recommendations.push('API response time is slow. Consider implementing caching.');
    }

    if (metrics.cacheHitRate < 0.8) {
      recommendations.push('Cache hit rate is low. Consider increasing cache TTL.');
    }

    return {
      metrics,
      recommendations
    };
  }

  /**
   * Clear performance data
   */
  clearPerformanceData(): void {
    this.startTimes.clear();
    this.apiTimes.clear();
    this.performanceMetrics$.next({
      loadTime: 0,
      renderTime: 0,
      memoryUsage: 0,
      bundleSize: 0,
      cacheHitRate: 0,
      apiResponseTime: 0
    });
  }
}
