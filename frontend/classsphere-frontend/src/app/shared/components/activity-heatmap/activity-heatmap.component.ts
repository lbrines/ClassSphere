import { Component, Input, OnInit, OnChanges, SimpleChanges, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface HeatmapData {
  date: string;
  value: number;
  label?: string;
}

export interface HeatmapConfig {
  startDate: Date;
  endDate: Date;
  colorScale: {
    min: string;
    max: string;
  };
  showTooltip: boolean;
  showLegend: boolean;
}

@Component({
  selector: 'app-activity-heatmap',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="heatmap-container">
      <div class="heatmap-header" *ngIf="title">
        <h3 class="heatmap-title">{{ title }}</h3>
        <div class="heatmap-subtitle" *ngIf="subtitle">{{ subtitle }}</div>
      </div>
      
      <div class="heatmap-content">
        <!-- Month labels -->
        <div class="month-labels">
          <div *ngFor="let month of monthLabels" class="month-label">
            {{ month }}
          </div>
        </div>
        
        <!-- Heatmap grid -->
        <div class="heatmap-grid">
          <div class="week-labels">
            <div *ngFor="let day of weekLabels" class="day-label">{{ day }}</div>
          </div>
          
          <div class="heatmap-squares">
            <div 
              *ngFor="let day of heatmapDays; trackBy: trackByDate"
              class="heatmap-square"
              [style.background-color]="getSquareColor(day.value)"
              [class.has-data]="day.value > 0"
              [title]="getTooltipText(day)"
              (mouseenter)="onSquareHover(day)"
              (mouseleave)="onSquareLeave()">
              <span class="square-value" *ngIf="day.value > 0">{{ day.value }}</span>
            </div>
          </div>
        </div>
        
        <!-- Legend -->
        <div class="heatmap-legend" *ngIf="config.showLegend">
          <span class="legend-label">Menos</span>
          <div class="legend-colors">
            <div 
              *ngFor="let color of legendColors" 
              class="legend-color"
              [style.background-color]="color">
            </div>
          </div>
          <span class="legend-label">Más</span>
        </div>
      </div>
      
      <!-- Tooltip -->
      <div 
        *ngIf="hoveredDay && config.showTooltip" 
        class="heatmap-tooltip"
        [style.left.px]="tooltipPosition.x"
        [style.top.px]="tooltipPosition.y">
        <div class="tooltip-content">
          <div class="tooltip-date">{{ hoveredDay.date }}</div>
          <div class="tooltip-value">{{ hoveredDay.value }} actividades</div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .heatmap-container {
      @apply bg-white rounded-lg shadow-lg p-6;
    }
    
    .heatmap-header {
      @apply mb-4;
    }
    
    .heatmap-title {
      @apply text-xl font-semibold text-gray-800 mb-1;
    }
    
    .heatmap-subtitle {
      @apply text-sm text-gray-600;
    }
    
    .heatmap-content {
      @apply relative;
    }
    
    .month-labels {
      @apply flex justify-between mb-2;
      margin-left: 30px;
    }
    
    .month-label {
      @apply text-xs text-gray-600 font-medium;
    }
    
    .heatmap-grid {
      @apply flex;
    }
    
    .week-labels {
      @apply flex flex-col mr-2;
    }
    
    .day-label {
      @apply text-xs text-gray-600 font-medium mb-1;
      height: 12px;
      line-height: 12px;
    }
    
    .heatmap-squares {
      @apply flex flex-wrap gap-1;
      width: calc(100% - 30px);
    }
    
    .heatmap-square {
      @apply w-3 h-3 rounded-sm border border-gray-200 cursor-pointer;
      @apply transition-all duration-200 hover:scale-110;
      @apply flex items-center justify-center;
    }
    
    .heatmap-square.has-data {
      @apply border-gray-300;
    }
    
    .square-value {
      @apply text-xs text-white font-bold;
      text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }
    
    .heatmap-legend {
      @apply flex items-center gap-2 mt-4;
    }
    
    .legend-label {
      @apply text-xs text-gray-600;
    }
    
    .legend-colors {
      @apply flex gap-1;
    }
    
    .legend-color {
      @apply w-3 h-3 rounded-sm;
    }
    
    .heatmap-tooltip {
      @apply absolute bg-gray-800 text-white px-3 py-2 rounded-lg shadow-lg;
      @apply text-sm z-50 pointer-events-none;
      transform: translate(-50%, -100%);
    }
    
    .tooltip-content {
      @apply text-center;
    }
    
    .tooltip-date {
      @apply font-medium;
    }
    
    .tooltip-value {
      @apply text-xs opacity-75;
    }
    
    /* Dark mode support */
    .dark .heatmap-container {
      @apply bg-gray-800;
    }
    
    .dark .heatmap-title {
      @apply text-gray-100;
    }
    
    .dark .heatmap-subtitle {
      @apply text-gray-400;
    }
    
    .dark .month-label,
    .dark .day-label,
    .dark .legend-label {
      @apply text-gray-400;
    }
    
    .dark .heatmap-square {
      @apply border-gray-600;
    }
  `]
})
export class ActivityHeatmapComponent implements OnInit, OnChanges {
  @Input() data: HeatmapData[] = [];
  @Input() title: string = '';
  @Input() subtitle: string = '';
  @Input() config: HeatmapConfig = {
    startDate: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000), // 1 year ago
    endDate: new Date(),
    colorScale: {
      min: '#ebedf0',
      max: '#216e39'
    },
    showTooltip: true,
    showLegend: true
  };

  public heatmapDays: HeatmapData[] = [];
  public monthLabels: string[] = [];
  public weekLabels = ['L', 'M', 'X', 'J', 'V', 'S', 'D'];
  public legendColors: string[] = [];
  public hoveredDay: HeatmapData | null = null;
  public tooltipPosition = { x: 0, y: 0 };

  ngOnInit() {
    this.generateHeatmapData();
    this.generateMonthLabels();
    this.generateLegendColors();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['data'] || changes['config']) {
      this.generateHeatmapData();
      this.generateMonthLabels();
      this.generateLegendColors();
    }
  }

  trackByDate(index: number, day: HeatmapData): string {
    return day.date;
  }

  private generateHeatmapData() {
    const days: HeatmapData[] = [];
    const startDate = new Date(this.config.startDate);
    const endDate = new Date(this.config.endDate);
    
    // Generate all days in the range
    for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
      const dateStr = d.toISOString().split('T')[0];
      const existingData = this.data.find(item => item.date === dateStr);
      
      days.push({
        date: dateStr,
        value: existingData?.value || 0,
        label: existingData?.label
      });
    }
    
    this.heatmapDays = days;
  }

  private generateMonthLabels() {
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                   'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    const labels: string[] = [];
    const startDate = new Date(this.config.startDate);
    const endDate = new Date(this.config.endDate);
    
    for (let d = new Date(startDate); d <= endDate; d.setMonth(d.getMonth() + 1)) {
      labels.push(months[d.getMonth()]);
    }
    
    this.monthLabels = labels;
  }

  private generateLegendColors() {
    const colors = [
      '#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127'
    ];
    this.legendColors = colors;
  }

  getSquareColor(value: number): string {
    if (value === 0) return this.config.colorScale.min;
    
    const maxValue = Math.max(...this.heatmapDays.map(d => d.value));
    const intensity = value / maxValue;
    
    // Interpolate between min and max colors
    return this.interpolateColor(this.config.colorScale.min, this.config.colorScale.max, intensity);
  }

  private interpolateColor(color1: string, color2: string, factor: number): string {
    const hex1 = color1.replace('#', '');
    const hex2 = color2.replace('#', '');
    
    const r1 = parseInt(hex1.substr(0, 2), 16);
    const g1 = parseInt(hex1.substr(2, 2), 16);
    const b1 = parseInt(hex1.substr(4, 2), 16);
    
    const r2 = parseInt(hex2.substr(0, 2), 16);
    const g2 = parseInt(hex2.substr(2, 2), 16);
    const b2 = parseInt(hex2.substr(4, 2), 16);
    
    const r = Math.round(r1 + (r2 - r1) * factor);
    const g = Math.round(g1 + (g2 - g1) * factor);
    const b = Math.round(b1 + (b2 - b1) * factor);
    
    return `rgb(${r}, ${g}, ${b})`;
  }

  getTooltipText(day: HeatmapData): string {
    const date = new Date(day.date);
    const formattedDate = date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    
    return `${formattedDate}: ${day.value} actividades`;
  }

  onSquareHover(day: HeatmapData) {
    this.hoveredDay = day;
    // Position tooltip near mouse cursor
    this.tooltipPosition = { x: 100, y: 50 }; // Simplified positioning
  }

  onSquareLeave() {
    this.hoveredDay = null;
  }
}
