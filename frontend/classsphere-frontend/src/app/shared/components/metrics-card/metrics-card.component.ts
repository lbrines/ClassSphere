import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface MetricCardData {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
    label?: string;
  };
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple' | 'indigo';
  format?: 'number' | 'percentage' | 'currency' | 'text';
}

@Component({
  selector: 'app-metrics-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="metrics-card" [ngClass]="getCardClasses()">
      <div class="card-header">
        <div class="card-icon" *ngIf="data.icon">
          <i [class]="data.icon"></i>
        </div>
        <div class="card-title">
          <h3 class="title">{{ data.title }}</h3>
          <p class="subtitle" *ngIf="data.subtitle">{{ data.subtitle }}</p>
        </div>
      </div>
      
      <div class="card-content">
        <div class="main-value">{{ formatValue(data.value) }}</div>
        
        <div class="trend" *ngIf="data.trend">
          <div class="trend-indicator" [ngClass]="getTrendClasses()">
            <i [class]="getTrendIcon()"></i>
            <span class="trend-value">{{ formatTrendValue(data.trend.value) }}</span>
            <span class="trend-label" *ngIf="data.trend.label">{{ data.trend.label }}</span>
          </div>
        </div>
      </div>
      
      <div class="card-footer" *ngIf="showFooter">
        <ng-content></ng-content>
      </div>
    </div>
  `,
  styles: [`
    .metrics-card {
      @apply bg-white rounded-lg shadow-md p-6 border border-gray-200 transition-all duration-200 hover:shadow-lg;
    }
    
    .card-header {
      @apply flex items-start justify-between mb-4;
    }
    
    .card-icon {
      @apply w-12 h-12 rounded-lg flex items-center justify-center text-white;
    }
    
    .card-icon i {
      @apply text-xl;
    }
    
    .card-title {
      @apply flex-1 ml-3;
    }
    
    .title {
      @apply text-lg font-semibold text-gray-800 mb-1;
    }
    
    .subtitle {
      @apply text-sm text-gray-600;
    }
    
    .card-content {
      @apply mb-4;
    }
    
    .main-value {
      @apply text-3xl font-bold text-gray-900 mb-2;
    }
    
    .trend {
      @apply flex items-center;
    }
    
    .trend-indicator {
      @apply flex items-center gap-1 px-2 py-1 rounded-full text-sm font-medium;
    }
    
    .trend-up {
      @apply bg-green-100 text-green-800;
    }
    
    .trend-down {
      @apply bg-red-100 text-red-800;
    }
    
    .trend-neutral {
      @apply bg-gray-100 text-gray-800;
    }
    
    .trend-value {
      @apply font-semibold;
    }
    
    .trend-label {
      @apply text-xs opacity-75;
    }
    
    .card-footer {
      @apply pt-4 border-t border-gray-100;
    }
    
    /* Color variants */
    .metrics-card.blue .card-icon {
      @apply bg-blue-500;
    }
    
    .metrics-card.green .card-icon {
      @apply bg-green-500;
    }
    
    .metrics-card.red .card-icon {
      @apply bg-red-500;
    }
    
    .metrics-card.yellow .card-icon {
      @apply bg-yellow-500;
    }
    
    .metrics-card.purple .card-icon {
      @apply bg-purple-500;
    }
    
    .metrics-card.indigo .card-icon {
      @apply bg-indigo-500;
    }
    
    /* Dark mode support */
    .dark .metrics-card {
      @apply bg-gray-800 border-gray-700;
    }
    
    .dark .title {
      @apply text-gray-100;
    }
    
    .dark .subtitle {
      @apply text-gray-400;
    }
    
    .dark .main-value {
      @apply text-gray-50;
    }
    
    .dark .card-footer {
      @apply border-gray-600;
    }
  `]
})
export class MetricsCardComponent {
  @Input() data: MetricCardData = {
    title: '',
    value: 0
  };
  @Input() showFooter: boolean = false;

  getCardClasses(): string {
    const baseClasses = 'metrics-card';
    const colorClass = this.data.color || 'blue';
    return `${baseClasses} ${colorClass}`;
  }

  getTrendClasses(): string {
    if (!this.data.trend) return '';
    
    switch (this.data.trend.direction) {
      case 'up':
        return 'trend-up';
      case 'down':
        return 'trend-down';
      default:
        return 'trend-neutral';
    }
  }

  getTrendIcon(): string {
    if (!this.data.trend) return '';
    
    switch (this.data.trend.direction) {
      case 'up':
        return 'fas fa-arrow-up';
      case 'down':
        return 'fas fa-arrow-down';
      default:
        return 'fas fa-minus';
    }
  }

  formatValue(value: string | number): string {
    if (typeof value === 'string') {
      return value;
    }

    switch (this.data.format) {
      case 'percentage':
        return `${value}%`;
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD'
        }).format(value);
      case 'number':
        return new Intl.NumberFormat('en-US').format(value);
      default:
        return value.toString();
    }
  }

  formatTrendValue(value: number): string {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value}%`;
  }
}
