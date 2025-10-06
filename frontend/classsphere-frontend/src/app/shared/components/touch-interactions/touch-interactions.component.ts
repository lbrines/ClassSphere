import { Component, Input, Output, EventEmitter, OnInit, OnDestroy, ElementRef, ViewChild, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface TouchGesture {
  type: 'swipe' | 'pinch' | 'pan' | 'tap' | 'longpress';
  direction?: 'left' | 'right' | 'up' | 'down';
  distance?: number;
  velocity?: number;
  scale?: number;
  duration?: number;
  center?: { x: number; y: number };
}

export interface TouchInteractionConfig {
  enableSwipe: boolean;
  enablePinch: boolean;
  enablePan: boolean;
  enableTap: boolean;
  enableLongPress: boolean;
  swipeThreshold: number;
  pinchThreshold: number;
  longPressDelay: number;
  tapTimeout: number;
  preventDefault: boolean;
}

@Component({
  selector: 'app-touch-interactions',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div 
      #touchContainer
      class="touch-container"
      [class.touch-active]="isTouchActive"
      [style.touch-action]="touchAction">
      <ng-content></ng-content>
      
      <!-- Touch Indicators (for debugging) -->
      <div 
        *ngIf="showTouchIndicators && touchPoints.length > 0"
        class="touch-indicators">
        <div 
          *ngFor="let point of touchPoints; trackBy: trackByTouchPoint"
          class="touch-point"
          [style.left.px]="point.x - 20"
          [style.top.px]="point.y - 20">
          <div class="touch-ring"></div>
          <div class="touch-center"></div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .touch-container {
      @apply relative w-full h-full;
      touch-action: manipulation;
    }

    .touch-container.touch-active {
      @apply select-none;
    }

    .touch-indicators {
      @apply absolute inset-0 pointer-events-none z-50;
    }

    .touch-point {
      @apply absolute w-10 h-10;
      animation: touch-indicator 0.5s ease-out;
    }

    .touch-ring {
      @apply absolute inset-0 rounded-full border-2 border-blue-500;
      @apply animate-ping opacity-75;
    }

    .touch-center {
      @apply absolute inset-2 rounded-full bg-blue-500;
    }

    @keyframes touch-indicator {
      0% {
        transform: scale(0.5);
        opacity: 1;
      }
      100% {
        transform: scale(1);
        opacity: 0;
      }
    }

    /* Disable text selection during touch */
    .touch-container.touch-active * {
      user-select: none;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
    }

    /* Prevent default touch behaviors */
    .touch-container.touch-active {
      -webkit-touch-callout: none;
      -webkit-user-select: none;
      -khtml-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
    }
  `]
})
export class TouchInteractionsComponent implements OnInit, OnDestroy {
  @ViewChild('touchContainer', { static: true }) touchContainer!: ElementRef;

  @Input() config: TouchInteractionConfig = {
    enableSwipe: true,
    enablePinch: true,
    enablePan: true,
    enableTap: true,
    enableLongPress: true,
    swipeThreshold: 50,
    pinchThreshold: 0.1,
    longPressDelay: 500,
    tapTimeout: 300,
    preventDefault: true
  };

  @Input() showTouchIndicators: boolean = false;
  @Input() touchAction: string = 'manipulation';

  @Output() gestureDetected = new EventEmitter<TouchGesture>();
  @Output() touchStart = new EventEmitter<TouchEvent>();
  @Output() touchMove = new EventEmitter<TouchEvent>();
  @Output() touchEnd = new EventEmitter<TouchEvent>();

  public isTouchActive: boolean = false;
  public touchPoints: Array<{ x: number; y: number; id: number }> = [];

  private touchStartTime: number = 0;
  private touchStartPositions: Map<number, { x: number; y: number; time: number }> = new Map();
  private longPressTimer: number | null = null;
  private lastTapTime: number = 0;
  private tapCount: number = 0;

  ngOnInit() {
    this.bindTouchEvents();
  }

  ngOnDestroy() {
    this.unbindTouchEvents();
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
    }
  }

  private bindTouchEvents(): void {
    const element = this.touchContainer.nativeElement;

    element.addEventListener('touchstart', this.onTouchStart.bind(this), { passive: false });
    element.addEventListener('touchmove', this.onTouchMove.bind(this), { passive: false });
    element.addEventListener('touchend', this.onTouchEnd.bind(this), { passive: false });
    element.addEventListener('touchcancel', this.onTouchEnd.bind(this), { passive: false });
  }

  private unbindTouchEvents(): void {
    const element = this.touchContainer.nativeElement;

    element.removeEventListener('touchstart', this.onTouchStart.bind(this));
    element.removeEventListener('touchmove', this.onTouchMove.bind(this));
    element.removeEventListener('touchend', this.onTouchEnd.bind(this));
    element.removeEventListener('touchcancel', this.onTouchEnd.bind(this));
  }

  private onTouchStart(event: TouchEvent): void {
    if (this.config.preventDefault) {
      event.preventDefault();
    }

    this.isTouchActive = true;
    this.touchStartTime = Date.now();
    this.updateTouchPoints(event);
    this.touchStart.emit(event);

    // Store initial touch positions
    for (let i = 0; i < event.touches.length; i++) {
      const touch = event.touches[i];
      this.touchStartPositions.set(touch.identifier, {
        x: touch.clientX,
        y: touch.clientY,
        time: this.touchStartTime
      });
    }

    // Start long press timer
    if (this.config.enableLongPress && event.touches.length === 1) {
      this.longPressTimer = window.setTimeout(() => {
        this.handleLongPress(event);
      }, this.config.longPressDelay);
    }

    // Handle double tap
    if (this.config.enableTap && event.touches.length === 1) {
      const currentTime = Date.now();
      const timeSinceLastTap = currentTime - this.lastTapTime;
      
      if (timeSinceLastTap < this.config.tapTimeout) {
        this.tapCount++;
      } else {
        this.tapCount = 1;
      }
      
      this.lastTapTime = currentTime;
    }
  }

  private onTouchMove(event: TouchEvent): void {
    if (this.config.preventDefault) {
      event.preventDefault();
    }

    this.updateTouchPoints(event);
    this.touchMove.emit(event);

    // Cancel long press if moved
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }

    // Detect gestures during move
    if (event.touches.length === 1) {
      this.detectSwipe(event);
    } else if (event.touches.length === 2) {
      this.detectPinch(event);
    }
  }

  private onTouchEnd(event: TouchEvent): void {
    if (this.config.preventDefault) {
      event.preventDefault();
    }

    this.isTouchActive = false;
    this.updateTouchPoints(event);
    this.touchEnd.emit(event);

    // Clear long press timer
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }

    // Detect tap
    if (this.config.enableTap && event.changedTouches.length === 1) {
      const touch = event.changedTouches[0];
      const startPos = this.touchStartPositions.get(touch.identifier);
      
      if (startPos) {
        const distance = Math.sqrt(
          Math.pow(touch.clientX - startPos.x, 2) + 
          Math.pow(touch.clientY - startPos.y, 2)
        );
        
        if (distance < 10) { // Small movement threshold
          this.handleTap(event);
        }
      }
    }

    // Clear touch positions
    for (let i = 0; i < event.changedTouches.length; i++) {
      const touch = event.changedTouches[i];
      this.touchStartPositions.delete(touch.identifier);
    }

    // Clear touch points after a delay
    setTimeout(() => {
      this.touchPoints = [];
    }, 100);
  }

  private updateTouchPoints(event: TouchEvent): void {
    this.touchPoints = [];
    for (let i = 0; i < event.touches.length; i++) {
      const touch = event.touches[i];
      this.touchPoints.push({
        x: touch.clientX,
        y: touch.clientY,
        id: touch.identifier
      });
    }
  }

  private detectSwipe(event: TouchEvent): void {
    if (!this.config.enableSwipe || event.touches.length !== 1) return;

    const touch = event.touches[0];
    const startPos = this.touchStartPositions.get(touch.identifier);
    
    if (!startPos) return;

    const deltaX = touch.clientX - startPos.x;
    const deltaY = touch.clientY - startPos.y;
    const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

    if (distance > this.config.swipeThreshold) {
      const duration = Date.now() - startPos.time;
      const velocity = distance / duration;
      
      let direction: 'left' | 'right' | 'up' | 'down';
      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        direction = deltaX > 0 ? 'right' : 'left';
      } else {
        direction = deltaY > 0 ? 'down' : 'up';
      }

      this.gestureDetected.emit({
        type: 'swipe',
        direction,
        distance,
        velocity,
        duration,
        center: { x: touch.clientX, y: touch.clientY }
      });
    }
  }

  private detectPinch(event: TouchEvent): void {
    if (!this.config.enablePinch || event.touches.length !== 2) return;

    const touch1 = event.touches[0];
    const touch2 = event.touches[1];
    
    const currentDistance = Math.sqrt(
      Math.pow(touch2.clientX - touch1.clientX, 2) + 
      Math.pow(touch2.clientY - touch1.clientY, 2)
    );

    const startPos1 = this.touchStartPositions.get(touch1.identifier);
    const startPos2 = this.touchStartPositions.get(touch2.identifier);
    
    if (!startPos1 || !startPos2) return;

    const startDistance = Math.sqrt(
      Math.pow(startPos2.x - startPos1.x, 2) + 
      Math.pow(startPos2.y - startPos1.y, 2)
    );

    const scale = currentDistance / startDistance;
    const scaleChange = Math.abs(scale - 1);

    if (scaleChange > this.config.pinchThreshold) {
      const centerX = (touch1.clientX + touch2.clientX) / 2;
      const centerY = (touch1.clientY + touch2.clientY) / 2;

      this.gestureDetected.emit({
        type: 'pinch',
        scale,
        center: { x: centerX, y: centerY }
      });
    }
  }

  private handleTap(event: TouchEvent): void {
    const touch = event.changedTouches[0];
    const duration = Date.now() - this.touchStartTime;

    this.gestureDetected.emit({
      type: 'tap',
      duration,
      center: { x: touch.clientX, y: touch.clientY }
    });
  }

  private handleLongPress(event: TouchEvent): void {
    const touch = event.touches[0];
    
    this.gestureDetected.emit({
      type: 'longpress',
      duration: this.config.longPressDelay,
      center: { x: touch.clientX, y: touch.clientY }
    });
  }

  trackByTouchPoint(index: number, point: any): number {
    return point.id;
  }

  // Public methods for external control
  public enableTouchIndicators(): void {
    this.showTouchIndicators = true;
  }

  public disableTouchIndicators(): void {
    this.showTouchIndicators = false;
  }

  public updateConfig(newConfig: Partial<TouchInteractionConfig>): void {
    this.config = { ...this.config, ...newConfig };
  }
}
