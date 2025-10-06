import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, from, of } from 'rxjs';
import { catchError, tap, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ChartLoaderService {
  private chartLoaded$ = new BehaviorSubject<boolean>(false);
  private chartLoading$ = new BehaviorSubject<boolean>(false);
  private chartInstance: any = null;
  private loadPromise: Promise<any> | null = null;

  constructor() {}

  /**
   * Get observable for chart loading state
   */
  get isChartLoaded(): Observable<boolean> {
    return this.chartLoaded$.asObservable();
  }

  /**
   * Get observable for chart loading progress
   */
  get isChartLoading(): Observable<boolean> {
    return this.chartLoading$.asObservable();
  }

  /**
   * Load Chart.js with optimized configuration
   */
  loadChart(): Observable<any> {
    if (this.chartInstance) {
      return of(this.chartInstance);
    }

    if (this.loadPromise) {
      return from(this.loadPromise);
    }

    this.chartLoading$.next(true);

    this.loadPromise = this.loadChartLibrary()
      .then(chart => {
        this.chartInstance = chart;
        this.chartLoaded$.next(true);
        this.chartLoading$.next(false);
        return chart;
      })
      .catch(error => {
        console.error('Failed to load Chart.js:', error);
        this.chartLoading$.next(false);
        throw error;
      });

    return from(this.loadPromise).pipe(
      catchError(error => {
        // Return a mock chart instance for graceful degradation
        return of(this.createMockChart());
      }),
      shareReplay(1)
    );
  }

  /**
   * Optimized Chart.js loading with tree shaking
   */
  private async loadChartLibrary(): Promise<any> {
    // Dynamic import with specific modules to reduce bundle size
    const { Chart, registerables } = await import('chart.js/auto');
    
    // Register only the modules we actually use
    Chart.register(...registerables);
    
    // Configure Chart.js for better performance
    Chart.defaults.responsive = true;
    Chart.defaults.maintainAspectRatio = false;
    Chart.defaults.interaction.intersect = false;
    Chart.defaults.animation = {
      duration: 750, // Reduced animation duration for better performance
      easing: 'easeInOutQuart'
    };

    // Optimize font loading
    Chart.defaults.font.family = "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.font.size = 12;

    return Chart;
  }

  /**
   * Create a mock chart for graceful degradation
   */
  private createMockChart(): any {
    return {
      register: () => {},
      defaults: {
        responsive: true,
        maintainAspectRatio: false
      }
    };
  }

  /**
   * Preload Chart.js for better user experience
   */
  preloadChart(): void {
    if (!this.chartInstance && !this.loadPromise) {
      this.loadChart().subscribe();
    }
  }

  /**
   * Get chart instance if loaded
   */
  getChartInstance(): any {
    return this.chartInstance;
  }

  /**
   * Clear chart instance (useful for testing)
   */
  clearChartInstance(): void {
    this.chartInstance = null;
    this.loadPromise = null;
    this.chartLoaded$.next(false);
  }
}
