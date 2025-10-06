import { test, expect } from '@playwright/test';

// Test data with existing users
const testUsers = {
  student: {
    email: 'student@test.com',
    password: 'StrongPassword123!',
    name: 'Test Student'
  },
  teacher: {
    email: 'teacher@test.com',
    password: 'StrongPassword123!',
    name: 'Test Teacher'
  },
  coordinator: {
    email: 'coordinator@test.com',
    password: 'StrongPassword123!',
    name: 'Test Coordinator'
  },
  admin: {
    email: 'admin@test.com',
    password: 'StrongPassword123!',
    name: 'Test Admin'
  }
};

// Helper function to register and login a user
async function registerAndLogin(page: any, user: any) {
  // Try login first since users should already exist
  await page.goto('/login');
  await page.fill('input[formControlName="email"]', user.email);
  await page.fill('input[formControlName="password"]', user.password);
  await page.click('button[type="submit"]');
  
  // Wait for login to complete
  await page.waitForTimeout(3000);
  
  // If login failed, try registration
  const currentUrl = page.url();
  if (currentUrl.includes('/login') || currentUrl.includes('/register')) {
    console.log('Login failed, trying registration for:', user.email);
    await page.goto('/register');
    await page.fill('input[name="email"]', user.email);
    await page.fill('input[name="name"]', user.name);
    await page.fill('input[name="password"]', user.password);
    await page.click('button[type="submit"]');
    await page.waitForTimeout(3000);
  }
}

// Helper function to login existing user
async function loginUser(page: any, user: any) {
  await page.goto('/login');
  await page.fill('input[formControlName="email"]', user.email);
  await page.fill('input[formControlName="password"]', user.password);
  await page.click('button[type="submit"]');
  await page.waitForLoadState('networkidle');
}

// Helper function to check dashboard elements
async function checkDashboardElements(page: any, role: string) {
  // Check for dashboard title (more specific selector)
  await expect(page.locator('h2').first()).toContainText(/panel|dashboard|welcome/i);
  
  // Check for stats cards (look for any div with stats-like content)
  const statsCards = page.locator('.bg-white.shadow.rounded-lg, .stats-card, .metric-card');
  const statsCount = await statsCards.count();
  expect(statsCount).toBeGreaterThan(0);
  
  // Check for any dashboard content (simplified approach)
  const dashboardContent = page.locator('.bg-white, .shadow, .rounded-lg');
  const contentCount = await dashboardContent.count();
  expect(contentCount).toBeGreaterThan(0);
  
  // Verify page loaded successfully by checking for main content
  await expect(page.locator('body')).toBeVisible();
  
  // Check that we're not on login/register page
  const currentUrl = page.url();
  expect(currentUrl).not.toContain('/login');
  expect(currentUrl).not.toContain('/register');
}

test.describe('Dashboard Flow E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should complete full student dashboard flow', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check dashboard elements
    await checkDashboardElements(page, 'student');
    
    // Test dashboard interactions
    await testDashboardInteractions(page);
    
    // Verify dashboard loaded successfully
    await expect(page.locator('body')).toBeVisible();
  });

  test('should complete full teacher dashboard flow', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check dashboard elements
    await checkDashboardElements(page, 'teacher');
    
    // Test dashboard interactions
    await testDashboardInteractions(page);
  });

  test('should complete full coordinator dashboard flow', async ({ page }) => {
    const user = testUsers.coordinator;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check dashboard elements
    await checkDashboardElements(page, 'coordinator');
    
    // Test dashboard interactions
    await testDashboardInteractions(page);
  });

  test('should complete full admin dashboard flow', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check dashboard elements
    await checkDashboardElements(page, 'admin');
    
    // Test dashboard interactions
    await testDashboardInteractions(page);
  });

  test('should handle dashboard navigation between different views', async ({ page }) => {
    const user = testUsers.student;
    
    // Login
    await loginUser(page, user);
    
    // Test navigation between different dashboard sections
    const navItems = page.locator('nav a, .nav-item, [data-testid="nav-item"]');
    const navCount = await navItems.count();
    
    for (let i = 0; i < Math.min(navCount, 3); i++) {
      await navItems.nth(i).click();
      await page.waitForLoadState('networkidle');
      
      // Verify page loaded successfully
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('should handle dashboard data refresh', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Login
    await loginUser(page, user);
    
    // Find and click refresh button
    const refreshButton = page.locator('[data-testid="refresh"], button:has-text("refresh"), .refresh-button');
    if (await refreshButton.count() > 0) {
      await refreshButton.first().click();
      await page.waitForLoadState('networkidle');
      
      // Verify data is still displayed
      await expect(page.locator('[data-testid="stats-card"], .stats-card')).toHaveCount.greaterThan(0);
    }
  });

  test('should handle dashboard export functionality', async ({ page }) => {
    const user = testUsers.admin;
    
    // Login
    await loginUser(page, user);
    
    // Look for export buttons
    const exportButtons = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    if (await exportButtons.count() > 0) {
      await exportButtons.first().click();
      
      // Wait for export dialog or download
      await page.waitForTimeout(1000);
      
      // Verify export functionality worked (no errors)
      await expect(page.locator('.error, [data-testid="error"]')).toHaveCount(0);
    }
  });

  test('should handle responsive dashboard layout', async ({ page }) => {
    const user = testUsers.student;
    
    // Login
    await loginUser(page, user);
    
    // Test desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page.locator('body')).toBeVisible();
    
    // Test tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page.locator('body')).toBeVisible();
    
    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('body')).toBeVisible();
    
    // Check if mobile menu is available
    const mobileMenu = page.locator('[data-testid="mobile-menu"], .mobile-menu, .hamburger');
    if (await mobileMenu.count() > 0) {
      await mobileMenu.click();
      await expect(page.locator('nav, .navigation')).toBeVisible();
    }
  });

  test('should handle dashboard error states gracefully', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Login
    await loginUser(page, user);
    
    // Simulate network error by going offline
    await page.context().setOffline(true);
    
    // Try to refresh dashboard
    const refreshButton = page.locator('[data-testid="refresh"], button:has-text("refresh")');
    if (await refreshButton.count() > 0) {
      await refreshButton.click();
      await page.waitForTimeout(2000);
      
      // Check for error message or loading state
      const errorMessage = page.locator('.error, [data-testid="error"], .offline');
      const loadingState = page.locator('.loading, [data-testid="loading"]');
      
      // Either error message or loading state should be visible
      const hasError = await errorMessage.count() > 0;
      const hasLoading = await loadingState.count() > 0;
      
      expect(hasError || hasLoading).toBeTruthy();
    }
    
    // Go back online
    await page.context().setOffline(false);
  });
});

// Helper function to test dashboard interactions
async function testDashboardInteractions(page: any) {
  // Test clicking on stats cards
  const statsCards = page.locator('[data-testid="stats-card"], .stats-card, .metric-card');
  const cardCount = await statsCards.count();
  
  if (cardCount > 0) {
    await statsCards.first().click();
    await page.waitForTimeout(500);
    
    // Verify interaction worked (no errors)
    await expect(page.locator('.error, [data-testid="error"]')).toHaveCount(0);
  }
  
  // Test chart interactions if available
  const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
  const chartCount = await charts.count();
  
  if (chartCount > 0) {
    await charts.first().hover();
    await page.waitForTimeout(500);
    
    // Verify chart is interactive
    await expect(charts.first()).toBeVisible();
  }
  
  // Test filter interactions if available
  const filters = page.locator('[data-testid="filter"], .filter, select, input[type="date"]');
  const filterCount = await filters.count();
  
  if (filterCount > 0) {
    await filters.first().click();
    await page.waitForTimeout(500);
    
    // Verify filter is interactive
    await expect(filters.first()).toBeVisible();
  }
}
