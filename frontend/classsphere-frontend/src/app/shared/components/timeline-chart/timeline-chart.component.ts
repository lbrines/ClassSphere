import { Component, Input, OnInit, OnChanges, SimpleChanges, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface TimelineDataPoint {
  date: string;
  value: number;
  label?: string;
  color?: string;
}

export interface TimelineConfig {
  height: number;
  showGrid: boolean;
  showPoints: boolean;
  showArea: boolean;
  curveType: 'linear' | 'smooth';
  color: string;
  areaOpacity: number;
}

@Component({
  selector: 'app-timeline-chart',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="timeline-container">
      <div class="timeline-header" *ngIf="title">
        <h3 class="timeline-title">{{ title }}</h3>
        <div class="timeline-subtitle" *ngIf="subtitle">{{ subtitle }}</div>
      </div>
      
      <div class="timeline-content">
        <svg 
          class="timeline-svg"
          [attr.width]="chartWidth"
          [attr.height]="config.height"
          [attr.viewBox]="'0 0 ' + chartWidth + ' ' + config.height">
          
          <!-- Grid lines -->
          <g class="grid-lines" *ngIf="config.showGrid">
            <line 
              *ngFor="let y of gridLines; trackBy: trackByIndex"
              [attr.x1]="0"
              [attr.y1]="y"
              [attr.x2]="chartWidth"
              [attr.y2]="y"
              class="grid-line">
            </line>
          </g>
          
          <!-- Area under curve -->
          <path 
            *ngIf="config.showArea && areaPath"
            [attr.d]="areaPath"
            [attr.fill]="config.color"
            [attr.fill-opacity]="config.areaOpacity"
            class="timeline-area">
          </path>
          
          <!-- Line path -->
          <path 
            *ngIf="linePath"
            [attr.d]="linePath"
            [attr.stroke]="config.color"
            [attr.stroke-width]="3"
            [attr.fill]="'none'"
            [attr.stroke-linecap]="'round'"
            [attr.stroke-linejoin]="'round'"
            class="timeline-line">
          </path>
          
          <!-- Data points -->
          <g class="data-points" *ngIf="config.showPoints">
            <circle 
              *ngFor="let point of dataPoints; trackBy: trackByIndex"
              [attr.cx]="point.x"
              [attr.cy]="point.y"
              [attr.r]="4"
              [attr.fill]="point.color || config.color"
              [attr.stroke]="'white'"
              [attr.stroke-width]="2"
              class="data-point"
              [title]="getPointTooltip(point)"
              (mouseenter)="onPointHover(point)"
              (mouseleave)="onPointLeave()">
            </circle>
          </g>
          
          <!-- Hover indicator -->
          <g *ngIf="hoveredPoint" class="hover-indicator">
            <line 
              [attr.x1]="hoveredPoint.x"
              [attr.y1]="0"
              [attr.x2]="hoveredPoint.x"
              [attr.y2]="config.height"
              class="hover-line">
            </line>
            <circle 
              [attr.cx]="hoveredPoint.x"
              [attr.cy]="hoveredPoint.y"
              [attr.r]="6"
              [attr.fill]="'white'"
              [attr.stroke]="hoveredPoint.color || config.color"
              [attr.stroke-width]="3"
              class="hover-point">
            </circle>
          </g>
        </svg>
        
        <!-- X-axis labels -->
        <div class="x-axis-labels">
          <div 
            *ngFor="let label of xAxisLabels; trackBy: trackByIndex"
            class="x-axis-label"
            [style.left.px]="label.x - 30">
            {{ label.text }}
          </div>
        </div>
        
        <!-- Y-axis labels -->
        <div class="y-axis-labels">
          <div 
            *ngFor="let label of yAxisLabels; trackBy: trackByIndex"
            class="y-axis-label"
            [style.top.px]="label.y - 8">
            {{ label.text }}
          </div>
        </div>
      </div>
      
      <!-- Tooltip -->
      <div 
        *ngIf="hoveredPoint && tooltipText" 
        class="timeline-tooltip"
        [style.left.px]="tooltipPosition.x"
        [style.top.px]="tooltipPosition.y">
        <div class="tooltip-content">
          <div class="tooltip-date">{{ tooltipText.date }}</div>
          <div class="tooltip-value">{{ tooltipText.value }}</div>
          <div class="tooltip-label" *ngIf="tooltipText.label">{{ tooltipText.label }}</div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .timeline-container {
      @apply bg-white rounded-lg shadow-lg p-6;
    }
    
    .timeline-header {
      @apply mb-4;
    }
    
    .timeline-title {
      @apply text-xl font-semibold text-gray-800 mb-1;
    }
    
    .timeline-subtitle {
      @apply text-sm text-gray-600;
    }
    
    .timeline-content {
      @apply relative;
    }
    
    .timeline-svg {
      @apply w-full;
    }
    
    .grid-line {
      @apply stroke-gray-200 stroke-1;
    }
    
    .timeline-area {
      @apply transition-all duration-300;
    }
    
    .timeline-line {
      @apply transition-all duration-300;
    }
    
    .data-point {
      @apply cursor-pointer transition-all duration-200;
    }
    
    .data-point:hover {
      r: 6px;
    }
    
    .hover-line {
      @apply stroke-gray-400 stroke-1 opacity-50;
    }
    
    .hover-point {
      @apply opacity-90;
    }
    
    .x-axis-labels {
      @apply relative mt-2;
      height: 20px;
    }
    
    .x-axis-label {
      @apply absolute text-xs text-gray-600 text-center;
      width: 60px;
    }
    
    .y-axis-labels {
      @apply absolute left-0 top-0;
      width: 40px;
    }
    
    .y-axis-label {
      @apply absolute text-xs text-gray-600 text-right;
      width: 40px;
    }
    
    .timeline-tooltip {
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
      @apply text-lg font-bold;
    }
    
    .tooltip-label {
      @apply text-xs opacity-75;
    }
    
    /* Dark mode support */
    .dark .timeline-container {
      @apply bg-gray-800;
    }
    
    .dark .timeline-title {
      @apply text-gray-100;
    }
    
    .dark .timeline-subtitle {
      @apply text-gray-400;
    }
    
    .dark .grid-line {
      @apply stroke-gray-600;
    }
    
    .dark .x-axis-label,
    .dark .y-axis-label {
      @apply text-gray-400;
    }
  `]
})
export class TimelineChartComponent implements OnInit, OnChanges {
  @Input() data: TimelineDataPoint[] = [];
  @Input() title: string = '';
  @Input() subtitle: string = '';
  @Input() config: TimelineConfig = {
    height: 200,
    showGrid: true,
    showPoints: true,
    showArea: true,
    curveType: 'smooth',
    color: '#3B82F6',
    areaOpacity: 0.2
  };

  public chartWidth: number = 800;
  public chartHeight: number = 200;
  public dataPoints: any[] = [];
  public linePath: string = '';
  public areaPath: string = '';
  public gridLines: number[] = [];
  public xAxisLabels: any[] = [];
  public yAxisLabels: any[] = [];
  public hoveredPoint: any = null;
  public tooltipText: any = null;
  public tooltipPosition = { x: 0, y: 0 };

  ngOnInit() {
    this.chartHeight = this.config.height;
    this.updateChart();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['data'] || changes['config']) {
      this.updateChart();
    }
  }

  trackByIndex(index: number): number {
    return index;
  }

  private updateChart() {
    if (!this.data || this.data.length === 0) return;

    this.calculateDimensions();
    this.generateDataPoints();
    this.generatePaths();
    this.generateGrid();
    this.generateAxisLabels();
  }

  private calculateDimensions() {
    this.chartWidth = Math.max(400, this.data.length * 60);
    this.chartHeight = this.config.height;
  }

  private generateDataPoints() {
    const minValue = Math.min(...this.data.map(d => d.value));
    const maxValue = Math.max(...this.data.map(d => d.value));
    const valueRange = maxValue - minValue;
    
    const padding = 40;
    const chartWidth = this.chartWidth - padding * 2;
    const chartHeight = this.chartHeight - padding * 2;
    
    this.dataPoints = this.data.map((point, index) => {
      const x = padding + (index / (this.data.length - 1)) * chartWidth;
      const y = padding + chartHeight - ((point.value - minValue) / valueRange) * chartHeight;
      
      return {
        x,
        y,
        value: point.value,
        date: point.date,
        label: point.label,
        color: point.color
      };
    });
  }

  private generatePaths() {
    if (this.dataPoints.length === 0) return;

    let linePath = `M ${this.dataPoints[0].x} ${this.dataPoints[0].y}`;
    let areaPath = `M ${this.dataPoints[0].x} ${this.chartHeight}`;

    for (let i = 1; i < this.dataPoints.length; i++) {
      const point = this.dataPoints[i];
      const prevPoint = this.dataPoints[i - 1];
      
      if (this.config.curveType === 'smooth') {
        const cp1x = prevPoint.x + (point.x - prevPoint.x) / 3;
        const cp1y = prevPoint.y;
        const cp2x = point.x - (point.x - prevPoint.x) / 3;
        const cp2y = point.y;
        
        linePath += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${point.x} ${point.y}`;
        areaPath += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${point.x} ${point.y}`;
      } else {
        linePath += ` L ${point.x} ${point.y}`;
        areaPath += ` L ${point.x} ${point.y}`;
      }
    }

    areaPath += ` L ${this.dataPoints[this.dataPoints.length - 1].x} ${this.chartHeight} Z`;

    this.linePath = linePath;
    this.areaPath = areaPath;
  }

  private generateGrid() {
    const gridCount = 5;
    this.gridLines = [];
    
    for (let i = 0; i <= gridCount; i++) {
      const y = 40 + (i / gridCount) * (this.chartHeight - 80);
      this.gridLines.push(y);
    }
  }

  private generateAxisLabels() {
    // X-axis labels
    this.xAxisLabels = this.dataPoints
      .filter((_, index) => index % Math.ceil(this.data.length / 6) === 0)
      .map(point => ({
        x: point.x,
        text: new Date(point.date).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })
      }));

    // Y-axis labels
    const minValue = Math.min(...this.data.map(d => d.value));
    const maxValue = Math.max(...this.data.map(d => d.value));
    const valueRange = maxValue - minValue;
    
    this.yAxisLabels = this.gridLines.map((y, index) => {
      const value = maxValue - (index / (this.gridLines.length - 1)) * valueRange;
      return {
        y,
        text: Math.round(value).toString()
      };
    });
  }

  getPointTooltip(point: any): string {
    const date = new Date(point.date).toLocaleDateString('es-ES');
    return `${date}: ${point.value}`;
  }

  onPointHover(point: any) {
    this.hoveredPoint = point;
    this.tooltipText = {
      date: new Date(point.date).toLocaleDateString('es-ES'),
      value: point.value,
      label: point.label
    };
    this.tooltipPosition = { x: point.x, y: point.y };
  }

  onPointLeave() {
    this.hoveredPoint = null;
    this.tooltipText = null;
  }
}
