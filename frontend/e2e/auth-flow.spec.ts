import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/auth/login');
  });

  test('should display login page correctly', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Welcome to ClassSphere');
    await expect(page.locator('#email')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should login with valid admin credentials', async ({ page }) => {
    // Fill credentials
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    
    // Submit
    await page.click('button[type="submit"]');
    
    // Should redirect to admin dashboard
    await expect(page).toHaveURL(/\/dashboard\/admin/);
    await expect(page.locator('h2')).toContainText('Administrator Overview');
  });

  test('should login with valid coordinator credentials', async ({ page }) => {
    await page.fill('#email', 'coordinator@classsphere.edu');
    await page.fill('#password', 'coord123');
    await page.click('button[type="submit"]');
    
    // Should redirect to coordinator dashboard
    await expect(page).toHaveURL(/\/dashboard\/coordinator/);
    await expect(page.locator('h2')).toContainText('Coordinator Console');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.fill('#email', 'invalid@test.com');
    await page.fill('#password', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    // Should stay on login page
    await expect(page).toHaveURL(/\/auth\/login/);
    
    // Should display error message
    await expect(page.locator('.text-red-300')).toBeVisible();
    await expect(page.locator('.text-red-300')).toContainText('Unable to sign in');
  });

  test('should validate email format', async ({ page }) => {
    await page.fill('#email', 'invalid-email');
    await page.fill('#password', 'password123');
    
    // Button should be disabled with invalid email
    const submitButton = page.locator('button[type="submit"]');
    await expect(submitButton).toBeDisabled();
    
    // Touch email field to trigger validation
    await page.locator('#email').blur();
    
    // Should show validation error
    await expect(page.locator('.text-red-400')).toBeVisible();
    await expect(page.locator('.text-red-400')).toContainText('valid email address');
  });

  test('should validate password minimum length', async ({ page }) => {
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', '123');
    
    // Password too short
    await expect(page.locator('button[type="submit"]')).toBeDisabled();
  });

  test('should disable submit button while pending', async ({ page }) => {
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    
    const submitButton = page.locator('button[type="submit"]');
    
    // Click submit
    await submitButton.click();
    
    // Button text should change
    await expect(submitButton).toContainText('Signing in');
  });
});

