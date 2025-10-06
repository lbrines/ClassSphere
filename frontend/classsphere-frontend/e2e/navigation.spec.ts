import { test, expect } from '@playwright/test';

test.describe('Navigation Flow', () => {
  test('should redirect to login from root', async ({ page }) => {
    // Go to root URL
    await page.goto('/');
    
    // Should redirect to login
    await expect(page).toHaveURL('/login');
  });

  test('should navigate between login and register', async ({ page }) => {
    // Start at login
    await page.goto('/login');
    await expect(page).toHaveURL('/login');
    
    // Navigate to register
    await page.click('text=Sign up here');
    await expect(page).toHaveURL('/register');
    
    // Navigate back to login
    await page.click('text=Sign in here');
    await expect(page).toHaveURL('/login');
  });

  test('should handle unknown routes', async ({ page }) => {
    // Go to unknown route
    await page.goto('/unknown-route');
    
    // Should redirect to login
    await expect(page).toHaveURL('/login');
  });

  test('should have consistent branding across pages', async ({ page }) => {
    // Check login page branding
    await page.goto('/login');
    await expect(page.locator('h2')).toContainText('ClassSphere');
    
    // Check register page branding
    await page.goto('/register');
    await expect(page.locator('h2')).toContainText('ClassSphere');
  });

  test('should be responsive across different viewports', async ({ page }) => {
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/login');
    await expect(page.locator('input[name="email"]')).toBeVisible();
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/login');
    await expect(page.locator('input[name="email"]')).toBeVisible();
    
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/login');
    await expect(page.locator('input[name="email"]')).toBeVisible();
  });
});
