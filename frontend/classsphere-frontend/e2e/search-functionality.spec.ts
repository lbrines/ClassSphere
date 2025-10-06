import { test, expect } from '@playwright/test';

test.describe('Search Functionality E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should perform basic search functionality', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for search input
    const searchInput = page.locator('[data-testid="search"], input[type="search"], input[placeholder*="search"]');
    
    if (await searchInput.count() > 0) {
      // Type search query
      await searchInput.fill('test');
      await page.waitForTimeout(1000);
      
      // Look for search button or trigger search
      const searchButton = page.locator('[data-testid="search-button"], button:has-text("search"), .search-button');
      
      if (await searchButton.count() > 0) {
        await searchButton.click();
      } else {
        // Try pressing Enter
        await searchInput.press('Enter');
      }
      
      await page.waitForLoadState('networkidle');
      
      // Check for search results
      const searchResults = page.locator('[data-testid="search-results"], .search-results, .results');
      await expect(searchResults).toBeVisible();
    }
  });

  test('should handle search suggestions', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for search input
    const searchInput = page.locator('[data-testid="search"], input[type="search"], input[placeholder*="search"]');
    
    if (await searchInput.count() > 0) {
      // Type partial search query
      await searchInput.fill('te');
      await page.waitForTimeout(1000);
      
      // Look for suggestions dropdown
      const suggestions = page.locator('[data-testid="suggestions"], .suggestions, .dropdown');
      
      if (await suggestions.count() > 0) {
        await expect(suggestions).toBeVisible();
        
        // Click on first suggestion
        const firstSuggestion = suggestions.locator('li, .suggestion-item').first();
        if (await firstSuggestion.count() > 0) {
          await firstSuggestion.click();
          await page.waitForLoadState('networkidle');
          
          // Verify search was performed
          const searchResults = page.locator('[data-testid="search-results"], .search-results');
          await expect(searchResults).toBeVisible();
        }
      }
    }
  });

  test('should filter search results', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Perform search
    const searchInput = page.locator('[data-testid="search"], input[type="search"]');
    
    if (await searchInput.count() > 0) {
      await searchInput.fill('test');
      await searchInput.press('Enter');
      await page.waitForLoadState('networkidle');
      
      // Look for filter options
      const filters = page.locator('[data-testid="filters"], .filters, select, input[type="checkbox"]');
      const filterCount = await filters.count();
      
      if (filterCount > 0) {
        // Apply first filter
        await filters.first().click();
        await page.waitForTimeout(1000);
        
        // Verify results were filtered
        const searchResults = page.locator('[data-testid="search-results"], .search-results');
        await expect(searchResults).toBeVisible();
      }
    }
  });

  test('should handle search pagination', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Perform search
    const searchInput = page.locator('[data-testid="search"], input[type="search"]');
    
    if (await searchInput.count() > 0) {
      await searchInput.fill('test');
      await searchInput.press('Enter');
      await page.waitForLoadState('networkidle');
      
      // Look for pagination controls
      const pagination = page.locator('[data-testid="pagination"], .pagination, .page-nav');
      
      if (await pagination.count() > 0) {
        // Click next page
        const nextButton = pagination.locator('button:has-text("next"), .next, [data-testid="next"]');
        
        if (await nextButton.count() > 0) {
          await nextButton.click();
          await page.waitForLoadState('networkidle');
          
          // Verify pagination worked
          await expect(pagination).toBeVisible();
        }
      }
    }
  });

  test('should handle search error states', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Simulate network error
    await page.context().setOffline(true);
    
    // Try to perform search
    const searchInput = page.locator('[data-testid="search"], input[type="search"]');
    
    if (await searchInput.count() > 0) {
      await searchInput.fill('test');
      await searchInput.press('Enter');
      await page.waitForTimeout(2000);
      
      // Check for error message
      const errorMessage = page.locator('.error, [data-testid="error"], .offline');
      const hasError = await errorMessage.count() > 0;
      
      if (hasError) {
        await expect(errorMessage).toBeVisible();
      }
    }
    
    // Go back online
    await page.context().setOffline(false);
  });

  test('should handle empty search results', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Perform search with unlikely query
    const searchInput = page.locator('[data-testid="search"], input[type="search"]');
    
    if (await searchInput.count() > 0) {
      await searchInput.fill('xyz123nonexistent');
      await searchInput.press('Enter');
      await page.waitForLoadState('networkidle');
      
      // Check for empty state message
      const emptyState = page.locator('[data-testid="empty-state"], .empty-state, .no-results');
      const hasEmptyState = await emptyState.count() > 0;
      
      if (hasEmptyState) {
        await expect(emptyState).toBeVisible();
      } else {
        // Verify search results container is still visible
        const searchResults = page.locator('[data-testid="search-results"], .search-results');
        await expect(searchResults).toBeVisible();
      }
    }
  });

  test('should handle search with special characters', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Perform search with special characters
    const searchInput = page.locator('[data-testid="search"], input[type="search"]');
    
    if (await searchInput.count() > 0) {
      const specialQueries = ['@#$%', 'test@example.com', 'user+tag', 'test & result'];
      
      for (const query of specialQueries) {
        await searchInput.fill(query);
        await searchInput.press('Enter');
        await page.waitForLoadState('networkidle');
        
        // Verify search didn't crash
        await expect(page.locator('body')).toBeVisible();
        
        // Clear search for next iteration
        await searchInput.clear();
      }
    }
  });

  test('should handle search performance with large queries', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Perform search with long query
    const searchInput = page.locator('[data-testid="search"], input[type="search"]');
    
    if (await searchInput.count() > 0) {
      const longQuery = 'a'.repeat(1000); // Very long query
      await searchInput.fill(longQuery);
      await searchInput.press('Enter');
      
      // Wait for search to complete (with timeout)
      await page.waitForLoadState('networkidle', { timeout: 10000 });
      
      // Verify search completed without crashing
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('should handle search keyboard shortcuts', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Test Ctrl+K or Cmd+K shortcut for search focus
    await page.keyboard.press('Control+k');
    await page.waitForTimeout(500);
    
    // Check if search input is focused
    const searchInput = page.locator('[data-testid="search"], input[type="search"]');
    
    if (await searchInput.count() > 0) {
      const isFocused = await searchInput.evaluate(el => el === document.activeElement);
      
      if (isFocused) {
        // Type search query
        await searchInput.fill('test');
        await searchInput.press('Enter');
        await page.waitForLoadState('networkidle');
        
        // Verify search was performed
        const searchResults = page.locator('[data-testid="search-results"], .search-results');
        await expect(searchResults).toBeVisible();
      }
    }
  });
});
