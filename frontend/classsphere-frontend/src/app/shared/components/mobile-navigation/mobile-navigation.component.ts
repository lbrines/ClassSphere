import { Component, Input, Output, EventEmitter, OnInit, OnDestroy, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router, NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs';
import { filter } from 'rxjs/operators';

export interface NavigationItem {
  id: string;
  label: string;
  icon: string;
  route: string;
  badge?: number;
  disabled?: boolean;
  children?: NavigationItem[];
}

@Component({
  selector: 'app-mobile-navigation',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <!-- Mobile Navigation Overlay -->
    <div 
      *ngIf="isOpen" 
      class="mobile-nav-overlay"
      (click)="closeNavigation()">
    </div>

    <!-- Mobile Navigation Drawer -->
    <nav 
      class="mobile-nav-drawer"
      [class.open]="isOpen"
      [class.closed]="!isOpen">
      
      <!-- Header -->
      <div class="mobile-nav-header">
        <div class="nav-brand">
          <div class="brand-logo">
            <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <div class="brand-text">
            <h2 class="brand-title">ClassSphere</h2>
            <p class="brand-subtitle">Plataforma Educativa</p>
          </div>
        </div>
        <button 
          class="nav-close-btn"
          (click)="closeNavigation()"
          aria-label="Cerrar navegación">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- User Info -->
      <div class="mobile-nav-user" *ngIf="userInfo">
        <div class="user-avatar">
          <img 
            [src]="userInfo.avatar || '/assets/images/default-avatar.png'" 
            [alt]="userInfo.name"
            class="avatar-image">
        </div>
        <div class="user-details">
          <h3 class="user-name">{{ userInfo.name }}</h3>
          <p class="user-role">{{ userInfo.role }}</p>
        </div>
      </div>

      <!-- Navigation Items -->
      <div class="mobile-nav-content">
        <ul class="nav-list">
          <li 
            *ngFor="let item of navigationItems; trackBy: trackByItem"
            class="nav-item"
            [class.active]="isActiveRoute(item.route)"
            [class.disabled]="item.disabled">
            
            <a 
              *ngIf="!item.children"
              [routerLink]="item.route"
              class="nav-link"
              (click)="onItemClick(item)"
              [class.disabled]="item.disabled">
              
              <div class="nav-icon">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" [attr.d]="getIconPath(item.icon)"/>
                </svg>
              </div>
              
              <span class="nav-label">{{ item.label }}</span>
              
              <div class="nav-badge" *ngIf="item.badge && item.badge > 0">
                <span class="badge-count">{{ item.badge }}</span>
              </div>
            </a>

            <!-- Dropdown for items with children -->
            <div *ngIf="item.children" class="nav-dropdown">
              <button 
                class="nav-link nav-dropdown-toggle"
                (click)="toggleDropdown(item.id)"
                [class.open]="openDropdowns.has(item.id)">
                
                <div class="nav-icon">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" [attr.d]="getIconPath(item.icon)"/>
                  </svg>
                </div>
                
                <span class="nav-label">{{ item.label }}</span>
                
                <div class="dropdown-arrow">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </div>
              </button>

              <ul class="nav-dropdown-menu" *ngIf="openDropdowns.has(item.id)">
                <li 
                  *ngFor="let child of item.children; trackBy: trackByItem"
                  class="nav-dropdown-item">
                  
                  <a 
                    [routerLink]="child.route"
                    class="nav-dropdown-link"
                    (click)="onItemClick(child)"
                    [class.disabled]="child.disabled">
                    
                    <div class="nav-icon-small">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" [attr.d]="getIconPath(child.icon)"/>
                      </svg>
                    </div>
                    
                    <span class="nav-label">{{ child.label }}</span>
                    
                    <div class="nav-badge" *ngIf="child.badge && child.badge > 0">
                      <span class="badge-count">{{ child.badge }}</span>
                    </div>
                  </a>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </div>

      <!-- Footer Actions -->
      <div class="mobile-nav-footer">
        <button 
          class="footer-btn"
          (click)="onSettingsClick()">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          <span>Configuración</span>
        </button>

        <button 
          class="footer-btn logout-btn"
          (click)="onLogoutClick()">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          <span>Cerrar Sesión</span>
        </button>
      </div>
    </nav>
  `,
  styles: [`
    .mobile-nav-overlay {
      @apply fixed inset-0 bg-black bg-opacity-50 z-40;
      backdrop-filter: blur(2px);
    }

    .mobile-nav-drawer {
      @apply fixed top-0 right-0 h-full w-80 bg-white shadow-xl z-50;
      @apply transform transition-transform duration-300 ease-in-out;
      @apply flex flex-col;
    }

    .mobile-nav-drawer.closed {
      @apply translate-x-full;
    }

    .mobile-nav-drawer.open {
      @apply translate-x-0;
    }

    .mobile-nav-header {
      @apply flex items-center justify-between p-4 border-b border-gray-200;
    }

    .nav-brand {
      @apply flex items-center space-x-3;
    }

    .brand-logo {
      @apply flex-shrink-0;
    }

    .brand-text {
      @apply flex flex-col;
    }

    .brand-title {
      @apply text-lg font-bold text-gray-900;
    }

    .brand-subtitle {
      @apply text-xs text-gray-500;
    }

    .nav-close-btn {
      @apply p-2 rounded-lg hover:bg-gray-100 transition-colors;
    }

    .mobile-nav-user {
      @apply flex items-center space-x-3 p-4 border-b border-gray-200;
    }

    .user-avatar {
      @apply flex-shrink-0;
    }

    .avatar-image {
      @apply w-10 h-10 rounded-full object-cover;
    }

    .user-details {
      @apply flex flex-col flex-1;
    }

    .user-name {
      @apply text-sm font-medium text-gray-900;
    }

    .user-role {
      @apply text-xs text-gray-500 capitalize;
    }

    .mobile-nav-content {
      @apply flex-1 overflow-y-auto;
    }

    .nav-list {
      @apply space-y-1 p-2;
    }

    .nav-item {
      @apply relative;
    }

    .nav-link {
      @apply flex items-center space-x-3 px-3 py-3 rounded-lg;
      @apply text-gray-700 hover:bg-gray-100 transition-colors;
      @apply relative;
    }

    .nav-link.active {
      @apply bg-blue-50 text-blue-700;
    }

    .nav-link.disabled {
      @apply opacity-50 cursor-not-allowed;
    }

    .nav-icon {
      @apply flex-shrink-0;
    }

    .nav-label {
      @apply flex-1 text-sm font-medium;
    }

    .nav-badge {
      @apply flex-shrink-0;
    }

    .badge-count {
      @apply bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-5 text-center;
    }

    .nav-dropdown-toggle {
      @apply w-full justify-between;
    }

    .dropdown-arrow {
      @apply flex-shrink-0 transition-transform duration-200;
    }

    .nav-dropdown-toggle.open .dropdown-arrow {
      @apply transform rotate-180;
    }

    .nav-dropdown-menu {
      @apply ml-8 mt-1 space-y-1;
    }

    .nav-dropdown-item {
      @apply relative;
    }

    .nav-dropdown-link {
      @apply flex items-center space-x-2 px-3 py-2 rounded-lg;
      @apply text-gray-600 hover:bg-gray-100 transition-colors;
      @apply text-sm;
    }

    .nav-icon-small {
      @apply flex-shrink-0;
    }

    .mobile-nav-footer {
      @apply border-t border-gray-200 p-4 space-y-2;
    }

    .footer-btn {
      @apply flex items-center space-x-3 w-full px-3 py-3 rounded-lg;
      @apply text-gray-700 hover:bg-gray-100 transition-colors;
      @apply text-sm font-medium;
    }

    .logout-btn {
      @apply text-red-600 hover:bg-red-50;
    }

    /* Dark mode support */
    .dark .mobile-nav-drawer {
      @apply bg-gray-800;
    }

    .dark .mobile-nav-header {
      @apply border-gray-700;
    }

    .dark .brand-title {
      @apply text-gray-100;
    }

    .dark .brand-subtitle {
      @apply text-gray-400;
    }

    .dark .mobile-nav-user {
      @apply border-gray-700;
    }

    .dark .user-name {
      @apply text-gray-100;
    }

    .dark .user-role {
      @apply text-gray-400;
    }

    .dark .nav-link {
      @apply text-gray-300 hover:bg-gray-700;
    }

    .dark .nav-link.active {
      @apply bg-blue-900 text-blue-200;
    }

    .dark .nav-dropdown-link {
      @apply text-gray-400 hover:bg-gray-700;
    }

    .dark .footer-btn {
      @apply text-gray-300 hover:bg-gray-700;
    }

    .dark .logout-btn {
      @apply text-red-400 hover:bg-red-900;
    }

    /* Responsive adjustments */
    @media (max-width: 320px) {
      .mobile-nav-drawer {
        @apply w-72;
      }
    }

    @media (max-width: 280px) {
      .mobile-nav-drawer {
        @apply w-64;
      }
      
      .brand-title {
        @apply text-base;
      }
      
      .nav-label {
        @apply text-xs;
      }
    }
  `]
})
export class MobileNavigationComponent implements OnInit, OnDestroy {
  @Input() isOpen: boolean = false;
  @Input() navigationItems: NavigationItem[] = [];
  @Input() userInfo: { name: string; role: string; avatar?: string } | null = null;

  @Output() close = new EventEmitter<void>();
  @Output() itemClick = new EventEmitter<NavigationItem>();
  @Output() settingsClick = new EventEmitter<void>();
  @Output() logoutClick = new EventEmitter<void>();

  public openDropdowns = new Set<string>();
  private routerSubscription: Subscription = new Subscription();

  constructor(private router: Router) {}

  ngOnInit() {
    // Listen to route changes to close navigation
    this.routerSubscription = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.closeNavigation();
      });
  }

  ngOnDestroy() {
    this.routerSubscription.unsubscribe();
  }

  @HostListener('document:keydown.escape', ['$event'])
  onEscapeKey(event: Event) {
    if (this.isOpen) {
      this.closeNavigation();
    }
  }

  @HostListener('document:touchstart', ['$event'])
  onTouchStart(event: TouchEvent) {
    // Close navigation on touch outside
    if (this.isOpen && !(event.target as Element).closest('.mobile-nav-drawer')) {
      this.closeNavigation();
    }
  }

  closeNavigation() {
    this.close.emit();
    this.openDropdowns.clear();
  }

  onItemClick(item: NavigationItem) {
    if (!item.disabled) {
      this.itemClick.emit(item);
    }
  }

  onSettingsClick() {
    this.settingsClick.emit();
  }

  onLogoutClick() {
    this.logoutClick.emit();
  }

  toggleDropdown(itemId: string) {
    if (this.openDropdowns.has(itemId)) {
      this.openDropdowns.delete(itemId);
    } else {
      this.openDropdowns.add(itemId);
    }
  }

  isActiveRoute(route: string): boolean {
    return this.router.url === route || this.router.url.startsWith(route + '/');
  }

  trackByItem(index: number, item: NavigationItem): string {
    return item.id;
  }

  getIconPath(iconName: string): string {
    const iconPaths: { [key: string]: string } = {
      'dashboard': 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z',
      'courses': 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
      'assignments': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
      'grades': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      'profile': 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
      'settings': 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z',
      'logout': 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1'
    };

    return iconPaths[iconName] || iconPaths['dashboard'];
  }
}
