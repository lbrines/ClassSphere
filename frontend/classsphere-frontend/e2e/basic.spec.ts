import { test, expect } from '@playwright/test';

test('should have E2E test infrastructure', async ({ page }) => {
  // This is a basic test to verify E2E infrastructure is working
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example Domain/);
});

test('should be able to navigate to a simple page', async ({ page }) => {
  // Test basic navigation capability
  await page.goto('/');
  await expect(page).toHaveURL(/login/);
  await expect(page.locator('h2')).toContainText('ClassSphere');
});

test('should handle basic form interactions', async ({ page }) => {
  // Test basic form interaction capability
  await page.goto('/register');
  await expect(page.locator('input[name="name"]')).toBeVisible();
  await page.fill('input[name="name"]', 'Test User');
  await expect(page.locator('input[name="name"]')).toHaveValue('Test User');
});

test('should handle basic JavaScript interactions', async ({ page }) => {
  // Test basic JavaScript interaction capability
  await page.goto('data:text/html,<html><body><button id="test">Click me</button><div id="result"></div><script>document.getElementById("test").onclick=function(){document.getElementById("result").innerHTML="Clicked!"}</script></body></html>');
  await page.click('#test');
  await expect(page.locator('#result')).toHaveText('Clicked!');
});

test('should handle responsive design', async ({ page }) => {
  // Test responsive design capability
  await page.goto('/login');
  
  // Test desktop viewport
  await page.setViewportSize({ width: 1920, height: 1080 });
  await expect(page.locator('h2')).toBeVisible();
  
  // Test mobile viewport
  await page.setViewportSize({ width: 375, height: 667 });
  await expect(page.locator('h2')).toBeVisible();
});
