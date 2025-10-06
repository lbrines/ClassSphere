import { Component, Input, OnInit, OnChanges, SimpleChanges, ViewChild, ElementRef, AfterViewInit, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartLoaderService } from '../../services/chart-loader.service';
import { Subject } from 'rxjs';
import { takeUntil, debounceTime } from 'rxjs/operators';

export interface ChartOptions {
  responsive: boolean;
  maintainAspectRatio: boolean;
  plugins?: {
    legend?: {
      position: 'top' | 'bottom' | 'left' | 'right';
    };
    title?: {
      display: boolean;
      text: string;
    };
  };
  scales?: {
    y?: {
      beginAtZero: boolean;
      max?: number;
    };
    x?: {
      beginAtZero: boolean;
    };
  };
}

@Component({
  selector: 'app-metrics-chart',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="chart-container">
      <div class="chart-header" *ngIf="title">
        <h3 class="chart-title">{{ title }}</h3>
        <div class="chart-subtitle" *ngIf="subtitle">{{ subtitle }}</div>
      </div>
      
      <div class="chart-wrapper">
        <!-- Loading skeleton -->
        <div *ngIf="isLoading" class="chart-loading">
          <div class="loading-skeleton"></div>
        </div>
        
        <!-- Chart canvas -->
        <canvas 
          *ngIf="!isLoading"
          #chartCanvas 
          [attr.width]="width" 
          [attr.height]="height"
          class="chart-canvas">
        </canvas>
      </div>
      
      <div class="chart-legend" *ngIf="showLegend && chartData">
        <div 
          *ngFor="let dataset of chartData.datasets; let i = index" 
          class="legend-item">
          <span 
            class="legend-color" 
            [style.background-color]="dataset.backgroundColor?.[0] || '#3B82F6'">
          </span>
          <span class="legend-label">{{ dataset.label }}</span>
          <span class="legend-value">{{ getTotalForDataset(dataset.data) }}</span>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .chart-container {
      @apply bg-white rounded-lg shadow-lg p-6;
    }
    
    .chart-header {
      @apply mb-4;
    }
    
    .chart-title {
      @apply text-xl font-semibold text-gray-800 mb-1;
    }
    
    .chart-subtitle {
      @apply text-sm text-gray-600;
    }
    
    .chart-wrapper {
      @apply relative mb-4;
      height: 300px;
    }
    
    .chart-canvas {
      @apply w-full h-full;
    }
    
    .chart-legend {
      @apply flex flex-wrap gap-4 justify-center;
    }
    
    .legend-item {
      @apply flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg;
    }
    
    .legend-color {
      @apply w-4 h-4 rounded-full;
    }
    
    .legend-label {
      @apply text-sm font-medium text-gray-700;
    }
    
    .legend-value {
      @apply text-sm font-bold text-blue-600;
    }
    
    /* Dark mode support */
    .dark .chart-container {
      @apply bg-gray-800;
    }
    
    .dark .chart-title {
      @apply text-gray-100;
    }
    
    .dark .chart-subtitle {
      @apply text-gray-400;
    }
    
    .dark .legend-item {
      @apply bg-gray-700;
    }
    
    .dark .legend-label {
      @apply text-gray-300;
    }
    
    /* Loading skeleton */
    .chart-loading {
      @apply flex items-center justify-center h-full;
    }
    
    .loading-skeleton {
      @apply w-full h-48 bg-gray-200 rounded-lg animate-pulse;
      background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
      background-size: 200% 100%;
      animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
      0% {
        background-position: 200% 0;
      }
      100% {
        background-position: -200% 0;
      }
    }
    
    .dark .loading-skeleton {
      @apply bg-gray-700;
      background: linear-gradient(90deg, #374151 25%, #4b5563 50%, #374151 75%);
    }
  `]
})
export class MetricsChartComponent implements OnInit, OnChanges, AfterViewInit, OnDestroy {
  @Input() chartData: any | null = null;
  @Input() chartType: 'bar' | 'line' | 'pie' | 'doughnut' = 'bar';
  @Input() title: string = '';
  @Input() subtitle: string = '';
  @Input() showLegend: boolean = true;
  @Input() width: number = 400;
  @Input() height: number = 300;
  @Input() options: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  @ViewChild('chartCanvas', { static: false }) chartCanvas!: ElementRef<HTMLCanvasElement>;
  
  private chart: any = null;
  private destroy$ = new Subject<void>();
  public isLoading = true;

  constructor(private chartLoaderService: ChartLoaderService) {}

  ngOnInit() {
    this.initializeChart();
  }

  ngAfterViewInit() {
    // Chart will be initialized after view is ready
    setTimeout(() => {
      this.renderChart();
    }, 100);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
    
    if (this.chart) {
      this.chart.destroy();
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['chartData'] && this.chartData) {
      this.updateChart();
    }
  }

  private initializeChart() {
    this.isLoading = true;
    
    this.chartLoaderService.loadChart()
      .pipe(
        takeUntil(this.destroy$),
        debounceTime(100) // Debounce to prevent rapid re-renders
      )
      .subscribe(chart => {
        this.isLoading = false;
        setTimeout(() => {
          this.renderChart();
        }, 50);
      });
  }

  private renderChart() {
    if (!this.chartData || !this.chartCanvas?.nativeElement) {
      return;
    }

    // Destroy existing chart
    if (this.chart) {
      this.chart.destroy();
    }

    const ctx = this.chartCanvas.nativeElement.getContext('2d');
    if (!ctx) return;

    // Default colors for datasets
    const defaultColors = [
      '#3B82F6', '#EF4444', '#10B981', '#F59E0B', 
      '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'
    ];

    // Apply default colors if not provided
    const processedData = {
      ...this.chartData,
      datasets: this.chartData.datasets.map((dataset: any, index: number) => ({
        ...dataset,
        backgroundColor: dataset.backgroundColor || [defaultColors[index % defaultColors.length]],
        borderColor: dataset.borderColor || [defaultColors[index % defaultColors.length]],
        borderWidth: dataset.borderWidth || 2
      }))
    };

    const Chart = this.chartLoaderService.getChartInstance();
    this.chart = new Chart(ctx, {
      type: this.chartType,
      data: processedData,
      options: this.options
    });
  }

  private updateChart() {
    if (this.chart && this.chartData) {
      this.chart.data = this.chartData;
      this.chart.update();
    } else {
      this.renderChart();
    }
  }

  getTotalForDataset(data: number[]): number {
    return data.reduce((sum, value) => sum + value, 0);
  }

}
