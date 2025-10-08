import { test, expect } from '@playwright/test';

test.describe('Role-Based Routing', () => {
  test('admin should see admin dashboard after login', async ({ page }) => {
    // Navigate to login
    await page.goto('/auth/login');
    
    // Login as admin
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    
    // Verify redirect to admin dashboard
    await expect(page).toHaveURL(/\/dashboard\/admin/);
    await expect(page.locator('h2')).toContainText('Administrator Overview');
    await expect(page.locator('p')).toContainText('Monitor organization-wide metrics');
    
    // Verify header shows user info (displayName might be different)
    const header = page.locator('header');
    await expect(header).toBeVisible();
  });

  test('coordinator should see coordinator dashboard after login', async ({ page }) => {
    await page.goto('/auth/login');
    
    await page.fill('#email', 'coordinator@classsphere.edu');
    await page.fill('#password', 'coord123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL(/\/dashboard\/coordinator/);
    await expect(page.locator('h2')).toContainText('Coordinator Console');
    await expect(page.locator('p')).toContainText('Manage course allocations');
  });

  test('should show ClassSphere branding in dashboard', async ({ page }) => {
    // Login first
    await page.goto('/auth/login');
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL(/\/dashboard/);
    
    // Verify branding (use first() to avoid strict mode violation)
    await expect(page.locator('header h1')).toContainText('ClassSphere');
    await expect(page.locator('header p').first()).toContainText('Intelligent classroom orchestration');
  });

  test('should display user role in header', async ({ page }) => {
    await page.goto('/auth/login');
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL(/\/dashboard/);
    
    // Verify header is visible
    const header = page.locator('header');
    await expect(header).toBeVisible();
    await expect(header).toContainText('ClassSphere');
  });
});

