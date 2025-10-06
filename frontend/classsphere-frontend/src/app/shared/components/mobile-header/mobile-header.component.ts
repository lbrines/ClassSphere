import { Component, Input, Output, EventEmitter, OnInit, OnDestroy, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

export interface MobileHeaderConfig {
  showBackButton: boolean;
  showMenuButton: boolean;
  showSearchButton: boolean;
  showNotificationButton: boolean;
  showProfileButton: boolean;
  title: string;
  subtitle?: string;
  backgroundColor?: string;
  textColor?: string;
}

@Component({
  selector: 'app-mobile-header',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <header 
      class="mobile-header"
      [style.background-color]="config.backgroundColor || '#ffffff'"
      [style.color]="config.textColor || '#1f2937'">
      
      <!-- Status Bar Spacer (for mobile devices) -->
      <div class="status-bar-spacer"></div>
      
      <!-- Main Header Content -->
      <div class="header-content">
        <!-- Left Section -->
        <div class="header-left">
          <!-- Back Button -->
          <button 
            *ngIf="config.showBackButton"
            class="header-btn back-btn"
            (click)="onBackClick()"
            aria-label="Volver">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>

          <!-- Menu Button -->
          <button 
            *ngIf="config.showMenuButton"
            class="header-btn menu-btn"
            (click)="onMenuClick()"
            aria-label="Abrir menú">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>

        <!-- Center Section -->
        <div class="header-center">
          <div class="header-title-section">
            <h1 class="header-title">{{ config.title }}</h1>
            <p class="header-subtitle" *ngIf="config.subtitle">{{ config.subtitle }}</p>
          </div>
        </div>

        <!-- Right Section -->
        <div class="header-right">
          <!-- Search Button -->
          <button 
            *ngIf="config.showSearchButton"
            class="header-btn search-btn"
            (click)="onSearchClick()"
            aria-label="Buscar">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </button>

          <!-- Notification Button -->
          <button 
            *ngIf="config.showNotificationButton"
            class="header-btn notification-btn"
            (click)="onNotificationClick()"
            aria-label="Notificaciones">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
            </svg>
            <!-- Notification Badge -->
            <span 
              *ngIf="notificationCount > 0" 
              class="notification-badge">
              {{ notificationCount > 99 ? '99+' : notificationCount }}
            </span>
          </button>

          <!-- Profile Button -->
          <button 
            *ngIf="config.showProfileButton"
            class="header-btn profile-btn"
            (click)="onProfileClick()"
            aria-label="Perfil">
            <img 
              [src]="userAvatar || '/assets/images/default-avatar.png'" 
              [alt]="userName"
              class="profile-avatar">
          </button>
        </div>
      </div>

      <!-- Search Bar (when active) -->
      <div 
        *ngIf="isSearchActive" 
        class="search-bar">
        <div class="search-input-container">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input 
            type="text" 
            class="search-input"
            placeholder="Buscar..."
            [(ngModel)]="searchQuery"
            (keyup.enter)="onSearchSubmit()"
            (blur)="onSearchBlur()"
            #searchInput>
          <button 
            class="search-clear-btn"
            (click)="clearSearch()"
            *ngIf="searchQuery">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Quick Actions (when search is active) -->
      <div 
        *ngIf="isSearchActive" 
        class="quick-actions">
        <button 
          *ngFor="let action of quickActions; trackBy: trackByAction"
          class="quick-action-btn"
          (click)="onQuickActionClick(action)">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" [attr.d]="getActionIcon(action.icon)"/>
          </svg>
          <span>{{ action.label }}</span>
        </button>
      </div>
    </header>
  `,
  styles: [`
    .mobile-header {
      @apply fixed top-0 left-0 right-0 z-40;
      @apply shadow-sm border-b border-gray-200;
      @apply transition-all duration-300;
    }

    .status-bar-spacer {
      height: env(safe-area-inset-top, 0px);
      @apply bg-current;
    }

    .header-content {
      @apply flex items-center justify-between px-4 py-3;
      min-height: 56px;
    }

    .header-left,
    .header-right {
      @apply flex items-center space-x-2;
      min-width: 80px;
    }

    .header-right {
      @apply justify-end;
    }

    .header-center {
      @apply flex-1 flex justify-center px-4;
    }

    .header-title-section {
      @apply text-center;
    }

    .header-title {
      @apply text-lg font-semibold truncate;
      max-width: 200px;
    }

    .header-subtitle {
      @apply text-xs opacity-75 truncate;
      max-width: 200px;
    }

    .header-btn {
      @apply p-2 rounded-lg transition-colors;
      @apply hover:bg-black hover:bg-opacity-5;
      @apply active:bg-black active:bg-opacity-10;
    }

    .profile-btn {
      @apply p-1;
    }

    .profile-avatar {
      @apply w-8 h-8 rounded-full object-cover;
      @apply border-2 border-current border-opacity-20;
    }

    .notification-btn {
      @apply relative;
    }

    .notification-badge {
      @apply absolute -top-1 -right-1;
      @apply bg-red-500 text-white text-xs rounded-full;
      @apply min-w-4 h-4 flex items-center justify-center;
      @apply px-1 text-center leading-none;
      font-size: 10px;
    }

    .search-bar {
      @apply px-4 pb-3;
    }

    .search-input-container {
      @apply relative flex items-center;
    }

    .search-icon {
      @apply absolute left-3 w-4 h-4 text-gray-400;
      pointer-events: none;
    }

    .search-input {
      @apply w-full pl-10 pr-10 py-2;
      @apply border border-gray-300 rounded-lg;
      @apply focus:outline-none focus:ring-2 focus:ring-blue-500;
      @apply text-sm;
    }

    .search-clear-btn {
      @apply absolute right-3 p-1;
      @apply text-gray-400 hover:text-gray-600;
    }

    .quick-actions {
      @apply px-4 pb-3 flex space-x-2;
    }

    .quick-action-btn {
      @apply flex items-center space-x-1 px-3 py-1;
      @apply bg-gray-100 rounded-full text-sm;
      @apply hover:bg-gray-200 transition-colors;
    }

    /* Dark mode support */
    .dark .mobile-header {
      @apply border-gray-700;
    }

    .dark .header-btn {
      @apply hover:bg-white hover:bg-opacity-10;
      @apply active:bg-white active:bg-opacity-20;
    }

    .dark .search-input {
      @apply bg-gray-800 border-gray-600 text-white;
    }

    .dark .quick-action-btn {
      @apply bg-gray-700 hover:bg-gray-600 text-gray-200;
    }

    /* Responsive adjustments */
    @media (max-width: 320px) {
      .header-title {
        max-width: 150px;
      }
      
      .header-subtitle {
        max-width: 150px;
      }
      
      .header-left,
      .header-right {
        min-width: 60px;
      }
    }

    /* iOS specific adjustments */
    @supports (-webkit-touch-callout: none) {
      .status-bar-spacer {
        height: 44px; /* iOS status bar height */
      }
    }

    /* Android specific adjustments */
    @media screen and (max-width: 767px) and (orientation: portrait) {
      .status-bar-spacer {
        height: 24px; /* Android status bar height */
      }
    }
  `]
})
export class MobileHeaderComponent implements OnInit, OnDestroy {
  @Input() config: MobileHeaderConfig = {
    showBackButton: false,
    showMenuButton: true,
    showSearchButton: true,
    showNotificationButton: true,
    showProfileButton: true,
    title: 'ClassSphere'
  };

  @Input() userAvatar: string = '';
  @Input() userName: string = '';
  @Input() notificationCount: number = 0;

  @Output() backClick = new EventEmitter<void>();
  @Output() menuClick = new EventEmitter<void>();
  @Output() searchClick = new EventEmitter<void>();
  @Output() notificationClick = new EventEmitter<void>();
  @Output() profileClick = new EventEmitter<void>();
  @Output() searchSubmit = new EventEmitter<string>();

  public isSearchActive: boolean = false;
  public searchQuery: string = '';
  public quickActions = [
    { id: 'courses', label: 'Cursos', icon: 'courses' },
    { id: 'assignments', label: 'Tareas', icon: 'assignments' },
    { id: 'grades', label: 'Calificaciones', icon: 'grades' },
    { id: 'profile', label: 'Perfil', icon: 'profile' }
  ];

  constructor(private router: Router) {}

  ngOnInit() {
    // Listen for back button on Android
    if (window.history) {
      window.addEventListener('popstate', this.handlePopState.bind(this));
    }
  }

  ngOnDestroy() {
    if (window.history) {
      window.removeEventListener('popstate', this.handlePopState.bind(this));
    }
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: Event) {
    // Adjust header for different screen sizes
    const target = event.target as Window;
    if (target.innerWidth > 768) {
      this.isSearchActive = false;
    }
  }

  private handlePopState(event: PopStateEvent) {
    if (this.config.showBackButton) {
      this.onBackClick();
    }
  }

  onBackClick() {
    this.backClick.emit();
    if (window.history.length > 1) {
      window.history.back();
    } else {
      this.router.navigate(['/']);
    }
  }

  onMenuClick() {
    this.menuClick.emit();
  }

  onSearchClick() {
    this.isSearchActive = !this.isSearchActive;
    this.searchClick.emit();
    
    if (this.isSearchActive) {
      // Focus search input after animation
      setTimeout(() => {
        const searchInput = document.querySelector('.search-input') as HTMLInputElement;
        if (searchInput) {
          searchInput.focus();
        }
      }, 100);
    }
  }

  onNotificationClick() {
    this.notificationClick.emit();
  }

  onProfileClick() {
    this.profileClick.emit();
  }

  onSearchSubmit() {
    if (this.searchQuery.trim()) {
      this.searchSubmit.emit(this.searchQuery);
      this.isSearchActive = false;
    }
  }

  onSearchBlur() {
    // Keep search active for a moment to allow quick actions
    setTimeout(() => {
      if (!this.searchQuery.trim()) {
        this.isSearchActive = false;
      }
    }, 200);
  }

  clearSearch() {
    this.searchQuery = '';
    const searchInput = document.querySelector('.search-input') as HTMLInputElement;
    if (searchInput) {
      searchInput.focus();
    }
  }

  onQuickActionClick(action: any) {
    this.searchQuery = action.label;
    this.onSearchSubmit();
  }

  trackByAction(index: number, action: any): string {
    return action.id;
  }

  getActionIcon(iconName: string): string {
    const iconPaths: { [key: string]: string } = {
      'courses': 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
      'assignments': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
      'grades': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      'profile': 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
    };

    return iconPaths[iconName] || iconPaths['courses'];
  }
}
