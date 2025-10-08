import { test, expect } from '@playwright/test';

test.describe('Protected Routes', () => {
  test('should redirect to login when accessing dashboard without authentication', async ({ page }) => {
    // Try to access dashboard directly
    await page.goto('/dashboard/admin');
    
    // Should redirect to login
    await expect(page).toHaveURL(/\/auth\/login/);
    await expect(page.locator('h1')).toContainText('Welcome to ClassSphere');
  });

  test('should redirect coordinator dashboard to login when not authenticated', async ({ page }) => {
    await page.goto('/dashboard/coordinator');
    await expect(page).toHaveURL(/\/auth\/login/);
  });

  test('should redirect teacher dashboard to login when not authenticated', async ({ page }) => {
    await page.goto('/dashboard/teacher');
    await expect(page).toHaveURL(/\/auth\/login/);
  });

  test('should redirect student dashboard to login when not authenticated', async ({ page }) => {
    await page.goto('/dashboard/student');
    await expect(page).toHaveURL(/\/auth\/login/);
  });

  test('should access dashboard after successful authentication', async ({ page }) => {
    // Login first
    await page.goto('/auth/login');
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    
    // Wait for redirect
    await expect(page).toHaveURL(/\/dashboard\/admin/);
    
    // Now navigate to other pages (should work because authenticated)
    await page.goto('/dashboard/admin');
    await expect(page).toHaveURL(/\/dashboard\/admin/);
    await expect(page.locator('h2')).toContainText('Administrator Overview');
  });

  test('should handle non-existent routes', async ({ page }) => {
    await page.goto('/non-existent-route');
    
    // Should either redirect to login or show not-found
    await page.waitForTimeout(500);
    
    const url = page.url();
    const hasLogin = url.includes('/auth/login');
    const hasNotFound = url.includes('not-found') || url.includes('404');
    const hasNotFoundText = await page.locator('text=404').isVisible().catch(() => false);
    
    // One of these should be true
    expect(hasLogin || hasNotFound || hasNotFoundText).toBeTruthy();
  });
});

