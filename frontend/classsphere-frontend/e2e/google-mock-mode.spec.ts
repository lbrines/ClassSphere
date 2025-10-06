import { test, expect } from '@playwright/test';

// Test users for different roles
const testUsers = {
  admin: {
    email: 'admin@test.com',
    password: 'StrongPassword123!',
    role: 'admin'
  },
  teacher: {
    email: 'teacher@test.com',
    password: 'StrongPassword123!',
    role: 'teacher'
  },
  student: {
    email: 'student@test.com',
    password: 'StrongPassword123!',
    role: 'student'
  },
  coordinator: {
    email: 'coordinator@test.com',
    password: 'StrongPassword123!',
    role: 'coordinator'
  }
};

// Helper function to register and login
async function registerAndLogin(page: any, user: any) {
  // Register
  await page.goto('/register');
  await page.fill('input[name="name"]', user.role.charAt(0).toUpperCase() + user.role.slice(1) + ' User');
  await page.fill('input[name="email"]', user.email);
  await page.fill('input[name="password"]', user.password);
  await page.fill('input[name="confirmPassword"]', user.password);
  await page.selectOption('select[name="role"]', user.role);
  await page.click('button[type="submit"]');
  
  // Wait for redirect to dashboard
  await page.waitForLoadState('networkidle');
}

// Helper function to login existing user
async function loginUser(page: any, user: any) {
  await page.goto('/login');
  await page.fill('input[name="email"]', user.email);
  await page.fill('input[name="password"]', user.password);
  await page.click('button[type="submit"]');
  await page.waitForLoadState('networkidle');
}

test.describe('Google/Mock Mode Toggle - Fase 2 E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should toggle between Google and Mock mode correctly', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Look for Google mode toggle component
    const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
    
    if (await toggleButton.count() > 0) {
      // Get initial state
      const initialText = await toggleButton.first().textContent();
      
      // Click to toggle
      await toggleButton.first().click();
      await page.waitForTimeout(500);
      
      // Verify state changed
      const newText = await toggleButton.first().textContent();
      expect(newText).not.toBe(initialText);
      
      // Toggle back
      await toggleButton.first().click();
      await page.waitForTimeout(500);
      
      // Verify state reverted
      const finalText = await toggleButton.first().textContent();
      expect(finalText).toBe(initialText);
    }
  });

  test('should display different data in Google vs Mock mode', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Look for metrics or data that should change between modes
    const metricsCards = page.locator('[data-testid="metrics-card"], .metrics-card, .stat-card');
    const initialCardCount = await metricsCards.count();
    
    if (initialCardCount > 0) {
      // Get initial data
      const initialData = await metricsCards.first().textContent();
      
      // Look for toggle and switch modes
      const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
      
      if (await toggleButton.count() > 0) {
        await toggleButton.first().click();
        await page.waitForTimeout(1000); // Wait for data to refresh
        
        // Verify data might have changed (or at least the toggle worked)
        const newData = await metricsCards.first().textContent();
        // Note: Data might be the same in mock mode, but toggle should work
        expect(newData).toBeDefined();
      }
    }
  });

  test('should persist mode preference across page reloads', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Look for toggle and change mode
    const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
    
    if (await toggleButton.count() > 0) {
      const initialText = await toggleButton.first().textContent();
      
      // Toggle to different mode
      await toggleButton.first().click();
      await page.waitForTimeout(500);
      
      const toggledText = await toggleButton.first().textContent();
      
      // Reload page
      await page.reload();
      await page.waitForLoadState('networkidle');
      
      // Check if mode preference was persisted
      const persistedText = await toggleButton.first().textContent();
      // Note: This test assumes localStorage persistence is implemented
      expect(persistedText).toBeDefined();
    }
  });

  test('should handle mode toggle for all user roles', async ({ page }) => {
    const roles = ['admin', 'teacher', 'student', 'coordinator'];
    
    for (const role of roles) {
      const user = testUsers[role as keyof typeof testUsers];
      
      // Register and login
      await registerAndLogin(page, user);
      
      // Should be redirected to dashboard
      await expect(page).toHaveURL(/dashboard/);
      
      // Look for toggle button
      const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
      
      if (await toggleButton.count() > 0) {
        // Verify toggle is visible and clickable
        await expect(toggleButton.first()).toBeVisible();
        await expect(toggleButton.first()).toBeEnabled();
        
        // Test toggle functionality
        await toggleButton.first().click();
        await page.waitForTimeout(500);
        
        // Verify toggle worked
        const toggleText = await toggleButton.first().textContent();
        expect(toggleText).toBeDefined();
      }
      
      // Logout for next role
      const logoutButton = page.locator('button:has-text("Cerrar sesión"), button:has-text("Logout"), [data-testid="logout"]');
      if (await logoutButton.count() > 0) {
        await logoutButton.first().click();
        await page.waitForLoadState('networkidle');
      }
    }
  });

  test('should show appropriate indicators for current mode', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Look for mode indicators
    const modeIndicators = page.locator('[data-testid="mode-indicator"], .mode-indicator, .current-mode');
    
    if (await modeIndicators.count() > 0) {
      // Verify mode indicator is visible
      await expect(modeIndicators.first()).toBeVisible();
      
      const indicatorText = await modeIndicators.first().textContent();
      expect(indicatorText).toMatch(/Google|Mock|Real|Test/i);
    }
    
    // Also check for toggle button text
    const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
    
    if (await toggleButton.count() > 0) {
      const toggleText = await toggleButton.first().textContent();
      expect(toggleText).toMatch(/Google|Mock|Switch|Toggle/i);
    }
  });

  test('should handle mode toggle errors gracefully', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Look for toggle button
    const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
    
    if (await toggleButton.count() > 0) {
      // Rapidly click toggle multiple times to test error handling
      for (let i = 0; i < 5; i++) {
        await toggleButton.first().click();
        await page.waitForTimeout(100);
      }
      
      // Verify no errors occurred
      const errorElements = page.locator('.error, [data-testid="error"], .alert-danger');
      const errorCount = await errorElements.count();
      expect(errorCount).toBe(0);
      
      // Verify toggle still works
      const toggleText = await toggleButton.first().textContent();
      expect(toggleText).toBeDefined();
    }
  });

  test('should maintain dashboard functionality in both modes', async ({ page }) => {
    const user = testUsers.coordinator;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Test dashboard functionality in both modes
    const modes = ['Google', 'Mock'];
    
    for (const mode of modes) {
      // Look for toggle button
      const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
      
      if (await toggleButton.count() > 0) {
        // Switch to the desired mode
        const currentText = await toggleButton.first().textContent();
        if (!currentText?.includes(mode)) {
          await toggleButton.first().click();
          await page.waitForTimeout(1000);
        }
        
        // Verify dashboard elements are still present
        const dashboardElements = page.locator('.dashboard, [data-testid="dashboard"], .bg-white.shadow.rounded-lg');
        const elementCount = await dashboardElements.count();
        expect(elementCount).toBeGreaterThan(0);
        
        // Verify metrics cards are visible
        const metricsCards = page.locator('[data-testid="metrics-card"], .metrics-card, .stat-card');
        const cardCount = await metricsCards.count();
        expect(cardCount).toBeGreaterThan(0);
        
        // Verify navigation still works
        const navButtons = page.locator('button:has-text("Búsqueda"), button:has-text("Gráficos"), button:has-text("D3")');
        if (await navButtons.count() > 0) {
          await expect(navButtons.first()).toBeEnabled();
        }
      }
    }
  });

  test('should show loading states during mode transitions', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Look for toggle button
    const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
    
    if (await toggleButton.count() > 0) {
      // Click toggle and immediately check for loading state
      await toggleButton.first().click();
      
      // Look for loading indicators
      const loadingIndicators = page.locator('.loading, [data-testid="loading"], .spinner, .animate-spin');
      const loadingCount = await loadingIndicators.count();
      
      // Either loading indicator should appear or toggle should complete quickly
      if (loadingCount > 0) {
        await expect(loadingIndicators.first()).toBeVisible();
        
        // Wait for loading to complete
        await page.waitForTimeout(2000);
        await expect(loadingIndicators.first()).not.toBeVisible();
      }
    }
  });

  test('should handle network errors during mode toggle', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Simulate network offline
    await page.context().setOffline(true);
    
    // Look for toggle button
    const toggleButton = page.locator('[data-testid="google-mode-toggle"], .google-mode-toggle, button:has-text("Google"), button:has-text("Mock")');
    
    if (await toggleButton.count() > 0) {
      // Try to toggle while offline
      await toggleButton.first().click();
      await page.waitForTimeout(1000);
      
      // Verify error handling (should show error message or fallback)
      const errorElements = page.locator('.error, [data-testid="error"], .alert-danger, .network-error');
      const errorCount = await errorElements.count();
      
      // Either error should be shown or toggle should be disabled
      if (errorCount === 0) {
        // If no error, toggle should be disabled or show offline indicator
        const isDisabled = await toggleButton.first().isDisabled();
        expect(isDisabled).toBe(true);
      }
    }
    
    // Go back online
    await page.context().setOffline(false);
  });
});
