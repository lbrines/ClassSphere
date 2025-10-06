import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, timer } from 'rxjs';
import { tap, catchError, switchMap, shareReplay } from 'rxjs/operators';

export interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number; // Time to live in milliseconds
}

@Injectable({
  providedIn: 'root'
})
export class MetricsCacheService {
  private cache = new Map<string, CacheEntry<any>>();
  private readonly DEFAULT_TTL = 5 * 60 * 1000; // 5 minutes
  private readonly REFRESH_INTERVAL = 30 * 1000; // 30 seconds

  constructor() {
    // Start cleanup timer
    this.startCleanupTimer();
  }

  /**
   * Get data from cache or execute function if not cached/expired
   */
  get<T>(
    key: string, 
    dataFn: () => Observable<T>, 
    ttl: number = this.DEFAULT_TTL
  ): Observable<T> {
    const cached = this.cache.get(key);
    
    if (cached && !this.isExpired(cached)) {
      return of(cached.data);
    }

    return dataFn().pipe(
      tap(data => {
        this.set(key, data, ttl);
      }),
      catchError(error => {
        console.warn(`Cache miss for key ${key}, returning cached data if available:`, error);
        return cached ? of(cached.data) : of(null);
      }),
      shareReplay(1)
    );
  }

  /**
   * Set data in cache
   */
  set<T>(key: string, data: T, ttl: number = this.DEFAULT_TTL): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
  }

  /**
   * Check if cache entry is expired
   */
  private isExpired(entry: CacheEntry<any>): boolean {
    return Date.now() - entry.timestamp > entry.ttl;
  }

  /**
   * Clear specific cache entry
   */
  clear(key: string): void {
    this.cache.delete(key);
  }

  /**
   * Clear all cache entries
   */
  clearAll(): void {
    this.cache.clear();
  }

  /**
   * Get cache size
   */
  getCacheSize(): number {
    return this.cache.size;
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): { size: number; keys: string[]; oldestEntry?: number } {
    const keys = Array.from(this.cache.keys());
    const timestamps = Array.from(this.cache.values()).map(entry => entry.timestamp);
    const oldestEntry = timestamps.length > 0 ? Math.min(...timestamps) : undefined;

    return {
      size: this.cache.size,
      keys,
      oldestEntry
    };
  }

  /**
   * Start cleanup timer to remove expired entries
   */
  private startCleanupTimer(): void {
    timer(this.REFRESH_INTERVAL, this.REFRESH_INTERVAL).subscribe(() => {
      this.cleanup();
    });
  }

  /**
   * Clean up expired cache entries
   */
  private cleanup(): void {
    const now = Date.now();
    const expiredKeys: string[] = [];

    for (const [key, entry] of this.cache.entries()) {
      if (now - entry.timestamp > entry.ttl) {
        expiredKeys.push(key);
      }
    }

    expiredKeys.forEach(key => {
      this.cache.delete(key);
    });

    if (expiredKeys.length > 0) {
      console.log(`Cleaned up ${expiredKeys.length} expired cache entries`);
    }
  }

  /**
   * Preload data into cache
   */
  preload<T>(key: string, dataFn: () => Observable<T>, ttl?: number): void {
    dataFn().subscribe(data => {
      this.set(key, data, ttl);
    });
  }

  /**
   * Get cached data synchronously (for immediate access)
   */
  getSync<T>(key: string): T | null {
    const cached = this.cache.get(key);
    return cached && !this.isExpired(cached) ? cached.data : null;
  }

  /**
   * Check if key exists in cache and is not expired
   */
  has(key: string): boolean {
    const cached = this.cache.get(key);
    return cached !== undefined && !this.isExpired(cached);
  }
}
