import { Component, Input, OnInit, OnChanges, SimpleChanges, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface RadarDataPoint {
  label: string;
  value: number;
  maxValue: number;
}

export interface RadarDataset {
  label: string;
  data: RadarDataPoint[];
  color: string;
  backgroundColor: string;
  borderWidth: number;
}

export interface RadarConfig {
  size: number;
  levels: number;
  showGrid: boolean;
  showLabels: boolean;
  showLegend: boolean;
  animation: boolean;
}

@Component({
  selector: 'app-radar-chart',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="radar-container">
      <div class="radar-header" *ngIf="title">
        <h3 class="radar-title">{{ title }}</h3>
        <div class="radar-subtitle" *ngIf="subtitle">{{ subtitle }}</div>
      </div>
      
      <div class="radar-content">
        <div class="radar-chart">
          <svg 
            class="radar-svg"
            [attr.width]="config.size"
            [attr.height]="config.size"
            [attr.viewBox]="'0 0 ' + config.size + ' ' + config.size">
            
            <!-- Grid circles -->
            <g class="grid-circles" *ngIf="config.showGrid">
              <circle 
                *ngFor="let radius of gridRadii; trackBy: trackByIndex"
                cx="50%"
                cy="50%"
                [attr.r]="radius"
                class="grid-circle">
              </circle>
            </g>
            
            <!-- Grid lines -->
            <g class="grid-lines" *ngIf="config.showGrid">
              <line 
                *ngFor="let line of gridLines; trackBy: trackByIndex"
                [attr.x1]="line.x1"
                [attr.y1]="line.y1"
                [attr.x2]="line.x2"
                [attr.y2]="line.y2"
                class="grid-line">
              </line>
            </g>
            
            <!-- Data areas -->
            <g class="data-areas">
              <polygon 
                *ngFor="let dataset of datasets; trackBy: trackByIndex"
                [attr.points]="getPolygonPoints(dataset)"
                [attr.fill]="dataset.backgroundColor"
                [attr.fill-opacity]="0.3"
                [attr.stroke]="dataset.color"
                [attr.stroke-width]="dataset.borderWidth"
                class="data-area">
              </polygon>
            </g>
            
            <!-- Data points -->
            <g class="data-points">
              <g *ngFor="let dataset of datasets; trackBy: trackByIndex">
                <circle 
                  *ngFor="let point of getDataPoints(dataset); trackBy: trackByIndex"
                  [attr.cx]="point.x"
                  [attr.cy]="point.y"
                  [attr.r]="4"
                  [attr.fill]="dataset.color"
                  [attr.stroke]="'white'"
                  [attr.stroke-width]="2"
                  class="data-point"
                  [title]="getPointTooltip(dataset, point)"
                  (mouseenter)="onPointHover(dataset, point)"
                  (mouseleave)="onPointLeave()">
                </circle>
              </g>
            </g>
            
            <!-- Labels -->
            <g class="axis-labels" *ngIf="config.showLabels">
              <text 
                *ngFor="let label of axisLabels; trackBy: trackByIndex"
                [attr.x]="label.x"
                [attr.y]="label.y"
                [attr.text-anchor]="label.anchor"
                class="axis-label">
                {{ label.text }}
              </text>
            </g>
          </svg>
        </div>
        
        <!-- Legend -->
        <div class="radar-legend" *ngIf="config.showLegend && datasets.length > 1">
          <div 
            *ngFor="let dataset of datasets; trackBy: trackByIndex"
            class="legend-item">
            <div 
              class="legend-color"
              [style.background-color]="dataset.color">
            </div>
            <span class="legend-label">{{ dataset.label }}</span>
          </div>
        </div>
      </div>
      
      <!-- Tooltip -->
      <div 
        *ngIf="hoveredPoint" 
        class="radar-tooltip"
        [style.left.px]="tooltipPosition.x"
        [style.top.px]="tooltipPosition.y">
        <div class="tooltip-content">
          <div class="tooltip-label">{{ hoveredPoint.label }}</div>
          <div class="tooltip-value">{{ hoveredPoint.value }}/{{ hoveredPoint.maxValue }}</div>
          <div class="tooltip-percentage">{{ getPercentage(hoveredPoint) }}%</div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .radar-container {
      @apply bg-white rounded-lg shadow-lg p-6;
    }
    
    .radar-header {
      @apply mb-4;
    }
    
    .radar-title {
      @apply text-xl font-semibold text-gray-800 mb-1;
    }
    
    .radar-subtitle {
      @apply text-sm text-gray-600;
    }
    
    .radar-content {
      @apply flex flex-col items-center;
    }
    
    .radar-chart {
      @apply relative mb-4;
    }
    
    .radar-svg {
      @apply w-full h-auto;
    }
    
    .grid-circle {
      @apply fill-none stroke-gray-200 stroke-1;
    }
    
    .grid-line {
      @apply stroke-gray-200 stroke-1;
    }
    
    .data-area {
      @apply transition-all duration-300;
    }
    
    .data-point {
      @apply cursor-pointer transition-all duration-200;
    }
    
    .data-point:hover {
      r: 6px;
    }
    
    .axis-label {
      @apply text-sm font-medium text-gray-700;
    }
    
    .radar-legend {
      @apply flex flex-wrap gap-4 justify-center;
    }
    
    .legend-item {
      @apply flex items-center gap-2;
    }
    
    .legend-color {
      @apply w-4 h-4 rounded-full;
    }
    
    .legend-label {
      @apply text-sm text-gray-600;
    }
    
    .radar-tooltip {
      @apply absolute bg-gray-800 text-white px-3 py-2 rounded-lg shadow-lg;
      @apply text-sm z-50 pointer-events-none;
      transform: translate(-50%, -100%);
    }
    
    .tooltip-content {
      @apply text-center;
    }
    
    .tooltip-label {
      @apply font-medium;
    }
    
    .tooltip-value {
      @apply text-lg font-bold;
    }
    
    .tooltip-percentage {
      @apply text-xs opacity-75;
    }
    
    /* Dark mode support */
    .dark .radar-container {
      @apply bg-gray-800;
    }
    
    .dark .radar-title {
      @apply text-gray-100;
    }
    
    .dark .radar-subtitle {
      @apply text-gray-400;
    }
    
    .dark .grid-circle,
    .dark .grid-line {
      @apply stroke-gray-600;
    }
    
    .dark .axis-label {
      @apply text-gray-300;
    }
    
    .dark .legend-label {
      @apply text-gray-400;
    }
  `]
})
export class RadarChartComponent implements OnInit, OnChanges {
  @Input() datasets: RadarDataset[] = [];
  @Input() title: string = '';
  @Input() subtitle: string = '';
  @Input() config: RadarConfig = {
    size: 300,
    levels: 5,
    showGrid: true,
    showLabels: true,
    showLegend: true,
    animation: true
  };

  public gridRadii: number[] = [];
  public gridLines: any[] = [];
  public axisLabels: any[] = [];
  public hoveredPoint: any = null;
  public tooltipPosition = { x: 0, y: 0 };

  ngOnInit() {
    this.generateGrid();
    this.generateAxisLabels();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['datasets'] || changes['config']) {
      this.generateGrid();
      this.generateAxisLabels();
    }
  }

  trackByIndex(index: number): number {
    return index;
  }

  private generateGrid() {
    const centerX = this.config.size / 2;
    const centerY = this.config.size / 2;
    const maxRadius = this.config.size / 2 - 50;
    
    // Generate grid circles
    this.gridRadii = [];
    for (let i = 1; i <= this.config.levels; i++) {
      const radius = (i / this.config.levels) * maxRadius;
      this.gridRadii.push(radius);
    }
    
    // Generate grid lines (spokes)
    if (this.datasets.length > 0) {
      const firstDataset = this.datasets[0];
      this.gridLines = firstDataset.data.map((_, index) => {
        const angle = (index / firstDataset.data.length) * 2 * Math.PI - Math.PI / 2;
        const x = centerX + Math.cos(angle) * maxRadius;
        const y = centerY + Math.sin(angle) * maxRadius;
        
        return {
          x1: centerX,
          y1: centerY,
          x2: x,
          y2: y
        };
      });
    }
  }

  private generateAxisLabels() {
    if (this.datasets.length === 0) return;
    
    const centerX = this.config.size / 2;
    const centerY = this.config.size / 2;
    const labelRadius = this.config.size / 2 - 20;
    
    const firstDataset = this.datasets[0];
    this.axisLabels = firstDataset.data.map((point, index) => {
      const angle = (index / firstDataset.data.length) * 2 * Math.PI - Math.PI / 2;
      const x = centerX + Math.cos(angle) * labelRadius;
      const y = centerY + Math.sin(angle) * labelRadius;
      
      let anchor = 'middle';
      if (x > centerX + 20) anchor = 'start';
      if (x < centerX - 20) anchor = 'end';
      
      return {
        x,
        y,
        text: point.label,
        anchor
      };
    });
  }

  getPolygonPoints(dataset: RadarDataset): string {
    const centerX = this.config.size / 2;
    const centerY = this.config.size / 2;
    const maxRadius = this.config.size / 2 - 50;
    
    return dataset.data.map((point, index) => {
      const angle = (index / dataset.data.length) * 2 * Math.PI - Math.PI / 2;
      const radius = (point.value / point.maxValue) * maxRadius;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      
      return `${x},${y}`;
    }).join(' ');
  }

  getDataPoints(dataset: RadarDataset): any[] {
    const centerX = this.config.size / 2;
    const centerY = this.config.size / 2;
    const maxRadius = this.config.size / 2 - 50;
    
    return dataset.data.map((point, index) => {
      const angle = (index / dataset.data.length) * 2 * Math.PI - Math.PI / 2;
      const radius = (point.value / point.maxValue) * maxRadius;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      
      return {
        x,
        y,
        label: point.label,
        value: point.value,
        maxValue: point.maxValue
      };
    });
  }

  getPointTooltip(dataset: RadarDataset, point: any): string {
    return `${dataset.label}: ${point.value}/${point.maxValue}`;
  }

  getPercentage(point: any): number {
    return Math.round((point.value / point.maxValue) * 100);
  }

  onPointHover(dataset: RadarDataset, point: any) {
    this.hoveredPoint = {
      ...point,
      datasetLabel: dataset.label
    };
    this.tooltipPosition = { x: point.x, y: point.y };
  }

  onPointLeave() {
    this.hoveredPoint = null;
  }
}
