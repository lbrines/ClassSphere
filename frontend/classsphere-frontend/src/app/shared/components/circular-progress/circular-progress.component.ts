import { Component, Input, OnInit, OnChanges, SimpleChanges, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface CircularProgressConfig {
  size: number;
  strokeWidth: number;
  color: string;
  backgroundColor: string;
  animationDuration: number;
  showPercentage: boolean;
  showValue: boolean;
  format: 'percentage' | 'number' | 'fraction';
}

@Component({
  selector: 'app-circular-progress',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="circular-progress-container" [style.width.px]="config.size" [style.height.px]="config.size">
      <svg 
        class="circular-progress-svg"
        [attr.width]="config.size"
        [attr.height]="config.size"
        viewBox="0 0 100 100">
        
        <!-- Background circle -->
        <circle
          class="progress-background"
          cx="50"
          cy="50"
          [attr.r]="radius"
          [attr.stroke-width]="strokeWidth"
          [attr.stroke]="config.backgroundColor"
          fill="none">
        </circle>
        
        <!-- Progress circle -->
        <circle
          class="progress-circle"
          cx="50"
          cy="50"
          [attr.r]="radius"
          [attr.stroke-width]="strokeWidth"
          [attr.stroke]="config.color"
          fill="none"
          [attr.stroke-dasharray]="circumference"
          [attr.stroke-dashoffset]="strokeDashoffset"
          [attr.stroke-linecap]="'round'"
          [style.animation-duration.ms]="config.animationDuration">
        </circle>
        
        <!-- Center content -->
        <foreignObject x="25" y="35" width="50" height="30">
          <div class="progress-content" xmlns="http://www.w3.org/1999/xhtml">
            <div class="progress-value" *ngIf="config.showValue">
              {{ formatValue(currentValue) }}
            </div>
            <div class="progress-percentage" *ngIf="config.showPercentage">
              {{ Math.round(currentValue) }}%
            </div>
            <div class="progress-label" *ngIf="label">
              {{ label }}
            </div>
          </div>
        </foreignObject>
      </svg>
    </div>
  `,
  styles: [`
    .circular-progress-container {
      @apply relative inline-block;
    }
    
    .circular-progress-svg {
      @apply transform -rotate-90;
    }
    
    .progress-background {
      @apply opacity-20;
    }
    
    .progress-circle {
      @apply transition-all duration-500 ease-in-out;
      animation: progress-animation 1s ease-in-out;
    }
    
    @keyframes progress-animation {
      from {
        stroke-dashoffset: 100;
      }
      to {
        stroke-dashoffset: var(--target-offset);
      }
    }
    
    .progress-content {
      @apply text-center;
    }
    
    .progress-value {
      @apply text-lg font-bold text-gray-800;
    }
    
    .progress-percentage {
      @apply text-sm font-medium text-gray-600;
    }
    
    .progress-label {
      @apply text-xs text-gray-500 mt-1;
    }
    
    /* Dark mode support */
    .dark .progress-value {
      @apply text-gray-100;
    }
    
    .dark .progress-percentage {
      @apply text-gray-300;
    }
    
    .dark .progress-label {
      @apply text-gray-400;
    }
    
    /* Size variants */
    .circular-progress-container.small {
      @apply scale-75;
    }
    
    .circular-progress-container.large {
      @apply scale-125;
    }
  `]
})
export class CircularProgressComponent implements OnInit, OnChanges {
  @Input() value: number = 0;
  @Input() max: number = 100;
  @Input() label: string = '';
  @Input() config: CircularProgressConfig = {
    size: 120,
    strokeWidth: 8,
    color: '#3B82F6',
    backgroundColor: '#E5E7EB',
    animationDuration: 1000,
    showPercentage: true,
    showValue: false,
    format: 'percentage'
  };

  public currentValue: number = 0;
  public radius: number = 0;
  public circumference: number = 0;
  public strokeDashoffset: number = 0;
  public strokeWidth: number = 0;

  // Expose Math to template
  public Math = Math;

  ngOnInit() {
    this.calculateDimensions();
    this.updateProgress();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['value'] || changes['max'] || changes['config']) {
      this.calculateDimensions();
      this.updateProgress();
    }
  }

  private calculateDimensions() {
    this.radius = (100 - this.config.strokeWidth) / 2;
    this.circumference = 2 * Math.PI * this.radius;
    this.strokeWidth = this.config.strokeWidth;
  }

  private updateProgress() {
    const percentage = Math.min(Math.max(this.value / this.max, 0), 1);
    this.currentValue = percentage * 100;
    this.strokeDashoffset = this.circumference - (percentage * this.circumference);
    
    // Set CSS custom property for animation
    document.documentElement.style.setProperty('--target-offset', this.strokeDashoffset.toString());
  }

  formatValue(value: number): string {
    switch (this.config.format) {
      case 'number':
        return Math.round(value).toString();
      case 'fraction':
        return `${Math.round(value)}/${this.max}`;
      case 'percentage':
      default:
        return `${Math.round(value)}%`;
    }
  }
}
