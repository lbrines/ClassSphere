import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GoogleService } from '../../services/google.service';

@Component({
  selector: 'app-google-mode-toggle',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="flex items-center space-x-3">
      <span class="text-sm text-gray-700">Modo Google:</span>
      <button
        (click)="toggleMode()"
        [class]="getToggleClass()"
        class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        [attr.aria-pressed]="isGoogleMode()"
        role="switch"
      >
        <span
          [class]="getSliderClass()"
          class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
        ></span>
      </button>
      <span class="text-sm font-medium" [class]="getModeTextClass()">
        {{ isGoogleMode() ? 'Real' : 'Mock' }}
      </span>
    </div>
  `,
  styles: []
})
export class GoogleModeToggleComponent implements OnInit {
  isGoogleMode = signal(true);
  isLoading = signal(false);

  constructor(private googleService: GoogleService) {}

  ngOnInit(): void {
    // Initialize with current mode from service
    this.isGoogleMode.set(this.googleService.isMockMode());
  }

  toggleMode(): void {
    if (this.isLoading()) return;

    this.isLoading.set(true);
    const newMode = !this.isGoogleMode();
    
    this.googleService.toggleMockMode(newMode).subscribe({
      next: (response) => {
        this.isGoogleMode.set(newMode);
        this.isLoading.set(false);
        console.log('Google mode toggled:', newMode ? 'Real' : 'Mock');
      },
      error: (error) => {
        console.error('Error toggling Google mode:', error);
        this.isLoading.set(false);
        // Revert the toggle on error
        this.isGoogleMode.set(!newMode);
      }
    });
  }

  getToggleClass(): string {
    if (this.isLoading()) {
      return 'bg-gray-300 cursor-not-allowed';
    }
    return this.isGoogleMode() 
      ? 'bg-indigo-600 hover:bg-indigo-700' 
      : 'bg-gray-200 hover:bg-gray-300';
  }

  getSliderClass(): string {
    if (this.isLoading()) {
      return 'translate-x-1';
    }
    return this.isGoogleMode() 
      ? 'translate-x-6' 
      : 'translate-x-1';
  }

  getModeTextClass(): string {
    if (this.isLoading()) {
      return 'text-gray-400';
    }
    return this.isGoogleMode() 
      ? 'text-indigo-600' 
      : 'text-gray-600';
  }
}
