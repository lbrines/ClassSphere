import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PerformanceService, PerformanceMetrics } from '../../services/performance.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

// Mock environment for now
const environment = {
  production: false
};

@Component({
  selector: 'app-performance-monitor',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="performance-monitor" *ngIf="showMonitor">
      <div class="monitor-header">
        <h3 class="monitor-title">Performance Monitor</h3>
        <button 
          class="toggle-button" 
          (click)="toggleMonitor()"
          [class.expanded]="isExpanded">
          {{ isExpanded ? '−' : '+' }}
        </button>
      </div>
      
      <div class="monitor-content" *ngIf="isExpanded">
        <!-- Performance Metrics -->
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-label">Load Time</div>
            <div class="metric-value" [class.warning]="metrics.loadTime > 3000">
              {{ metrics.loadTime | number:'1.0-0' }}ms
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-label">Render Time</div>
            <div class="metric-value" [class.warning]="metrics.renderTime > 100">
              {{ metrics.renderTime | number:'1.0-0' }}ms
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-label">Memory Usage</div>
            <div class="metric-value" [class.warning]="metrics.memoryUsage > 50">
              {{ metrics.memoryUsage | number:'1.1-1' }}MB
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-label">Bundle Size</div>
            <div class="metric-value">
              {{ metrics.bundleSize | number:'1.1-1' }}KB
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-label">Cache Hit Rate</div>
            <div class="metric-value" [class.good]="metrics.cacheHitRate > 0.8">
              {{ (metrics.cacheHitRate * 100) | number:'1.0-0' }}%
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-label">API Response</div>
            <div class="metric-value" [class.warning]="metrics.apiResponseTime > 1000">
              {{ metrics.apiResponseTime | number:'1.0-0' }}ms
            </div>
          </div>
        </div>
        
        <!-- Performance Recommendations -->
        <div class="recommendations" *ngIf="recommendations.length > 0">
          <h4 class="recommendations-title">Recommendations</h4>
          <ul class="recommendations-list">
            <li *ngFor="let rec of recommendations" class="recommendation-item">
              {{ rec }}
            </li>
          </ul>
        </div>
        
        <!-- Performance Actions -->
        <div class="performance-actions">
          <button class="action-button" (click)="clearCache()">
            Clear Cache
          </button>
          <button class="action-button" (click)="refreshMetrics()">
            Refresh Metrics
          </button>
          <button class="action-button" (click)="exportReport()">
            Export Report
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .performance-monitor {
      @apply fixed bottom-4 right-4 bg-white rounded-lg shadow-lg border border-gray-200 z-50;
      width: 320px;
      max-height: 80vh;
      overflow-y: auto;
    }
    
    .monitor-header {
      @apply flex items-center justify-between p-4 border-b border-gray-200;
    }
    
    .monitor-title {
      @apply text-lg font-semibold text-gray-800 m-0;
    }
    
    .toggle-button {
      @apply w-8 h-8 rounded-full bg-blue-500 text-white font-bold flex items-center justify-center;
      @apply hover:bg-blue-600 transition-colors duration-200;
    }
    
    .toggle-button.expanded {
      @apply bg-red-500 hover:bg-red-600;
    }
    
    .monitor-content {
      @apply p-4;
    }
    
    .metrics-grid {
      @apply grid grid-cols-2 gap-3 mb-4;
    }
    
    .metric-card {
      @apply bg-gray-50 rounded-lg p-3 text-center;
    }
    
    .metric-label {
      @apply text-xs text-gray-600 mb-1;
    }
    
    .metric-value {
      @apply text-lg font-bold text-gray-800;
    }
    
    .metric-value.warning {
      @apply text-red-600;
    }
    
    .metric-value.good {
      @apply text-green-600;
    }
    
    .recommendations {
      @apply mb-4;
    }
    
    .recommendations-title {
      @apply text-sm font-semibold text-gray-700 mb-2;
    }
    
    .recommendations-list {
      @apply list-disc list-inside text-sm text-gray-600 space-y-1;
    }
    
    .recommendation-item {
      @apply leading-relaxed;
    }
    
    .performance-actions {
      @apply flex flex-wrap gap-2;
    }
    
    .action-button {
      @apply px-3 py-1 bg-blue-500 text-white text-xs rounded;
      @apply hover:bg-blue-600 transition-colors duration-200;
    }
    
    /* Dark mode support */
    .dark .performance-monitor {
      @apply bg-gray-800 border-gray-600;
    }
    
    .dark .monitor-title {
      @apply text-gray-100;
    }
    
    .dark .metric-card {
      @apply bg-gray-700;
    }
    
    .dark .metric-label {
      @apply text-gray-400;
    }
    
    .dark .metric-value {
      @apply text-gray-100;
    }
    
    .dark .recommendations-title {
      @apply text-gray-300;
    }
    
    .dark .recommendation-item {
      @apply text-gray-400;
    }
  `]
})
export class PerformanceMonitorComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  
  public metrics: PerformanceMetrics = {
    loadTime: 0,
    renderTime: 0,
    memoryUsage: 0,
    bundleSize: 0,
    cacheHitRate: 0,
    apiResponseTime: 0
  };
  
  public recommendations: string[] = [];
  public showMonitor = false;
  public isExpanded = false;

  constructor(private performanceService: PerformanceService) {}

  ngOnInit() {
    // Only show in development mode
    this.showMonitor = !environment.production;
    
    if (this.showMonitor) {
      this.performanceService.getPerformanceMetrics()
        .pipe(takeUntil(this.destroy$))
        .subscribe(metrics => {
          this.metrics = metrics;
          this.updateRecommendations();
        });
    }
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  toggleMonitor() {
    this.isExpanded = !this.isExpanded;
  }

  private updateRecommendations() {
    const report = this.performanceService.getPerformanceReport();
    this.recommendations = report.recommendations;
  }

  clearCache() {
    // This would clear the metrics cache
    console.log('Clearing cache...');
    // Implementation would depend on your cache service
  }

  refreshMetrics() {
    this.performanceService.clearPerformanceData();
    console.log('Refreshing performance metrics...');
  }

  exportReport() {
    const report = this.performanceService.getPerformanceReport();
    const dataStr = JSON.stringify(report, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'performance-report.json';
    link.click();
    URL.revokeObjectURL(url);
  }
}
