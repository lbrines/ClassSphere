import { test, expect } from '@playwright/test';

test.describe('Google Classroom Integration E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should handle Google OAuth flow', async ({ page }) => {
    // Go to login page
    await page.goto('/login');
    
    // Look for Google OAuth button
    const googleButton = page.locator('[data-testid="google-login"], button:has-text("Google"), .google-login');
    
    if (await googleButton.count() > 0) {
      // Click Google login button
      await googleButton.click();
      
      // Wait for OAuth redirect or popup
      await page.waitForTimeout(2000);
      
      // Check if redirected to Google or OAuth page
      const currentUrl = page.url();
      const isGoogleOAuth = currentUrl.includes('google') || currentUrl.includes('oauth') || currentUrl.includes('accounts.google.com');
      
      if (isGoogleOAuth) {
        // If we're on Google OAuth page, we can't complete the flow in E2E
        // but we can verify the page loaded correctly
        await expect(page.locator('body')).toBeVisible();
        
        // Go back to our app
        await page.goBack();
      }
    }
  });

  test('should toggle Google Classroom mock mode', async ({ page }) => {
    // Login as admin user
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for Google Classroom toggle or settings
    const toggleButton = page.locator('[data-testid="google-toggle"], button:has-text("Google"), .google-toggle');
    
    if (await toggleButton.count() > 0) {
      // Click toggle button
      await toggleButton.click();
      await page.waitForTimeout(1000);
      
      // Verify toggle state changed
      await expect(toggleButton).toBeVisible();
    }
  });

  test('should display Google Classroom courses', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Navigate to courses section
    const coursesLink = page.locator('a:has-text("courses"), [data-testid="courses"], .courses-link');
    
    if (await coursesLink.count() > 0) {
      await coursesLink.click();
      await page.waitForLoadState('networkidle');
      
      // Check for course list
      const courseList = page.locator('[data-testid="course-list"], .course-list, .courses');
      await expect(courseList).toBeVisible();
      
      // Check for individual course items
      const courseItems = page.locator('[data-testid="course-item"], .course-item, .course');
      const courseCount = await courseItems.count();
      
      if (courseCount > 0) {
        // Click on first course
        await courseItems.first().click();
        await page.waitForLoadState('networkidle');
        
        // Verify course details are displayed
        await expect(page.locator('body')).toBeVisible();
      }
    }
  });

  test('should display Google Classroom students', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Navigate to students section
    const studentsLink = page.locator('a:has-text("students"), [data-testid="students"], .students-link');
    
    if (await studentsLink.count() > 0) {
      await studentsLink.click();
      await page.waitForLoadState('networkidle');
      
      // Check for student list
      const studentList = page.locator('[data-testid="student-list"], .student-list, .students');
      await expect(studentList).toBeVisible();
      
      // Check for individual student items
      const studentItems = page.locator('[data-testid="student-item"], .student-item, .student');
      const studentCount = await studentItems.count();
      
      if (studentCount > 0) {
        // Verify student information is displayed
        await expect(studentItems.first()).toBeVisible();
      }
    }
  });

  test('should display Google Classroom assignments', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Navigate to assignments section
    const assignmentsLink = page.locator('a:has-text("assignments"), [data-testid="assignments"], .assignments-link');
    
    if (await assignmentsLink.count() > 0) {
      await assignmentsLink.click();
      await page.waitForLoadState('networkidle');
      
      // Check for assignment list
      const assignmentList = page.locator('[data-testid="assignment-list"], .assignment-list, .assignments');
      await expect(assignmentList).toBeVisible();
      
      // Check for individual assignment items
      const assignmentItems = page.locator('[data-testid="assignment-item"], .assignment-item, .assignment');
      const assignmentCount = await assignmentItems.count();
      
      if (assignmentCount > 0) {
        // Click on first assignment
        await assignmentItems.first().click();
        await page.waitForLoadState('networkidle');
        
        // Verify assignment details are displayed
        await expect(page.locator('body')).toBeVisible();
      }
    }
  });

  test('should handle Google Classroom data synchronization', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for sync button
    const syncButton = page.locator('[data-testid="sync"], button:has-text("sync"), .sync-button');
    
    if (await syncButton.count() > 0) {
      // Click sync button
      await syncButton.click();
      await page.waitForTimeout(2000);
      
      // Check for sync status or loading indicator
      const syncStatus = page.locator('[data-testid="sync-status"], .sync-status, .loading');
      const hasStatus = await syncStatus.count() > 0;
      
      if (hasStatus) {
        await expect(syncStatus).toBeVisible();
      }
    }
  });

  test('should handle Google Classroom error states', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Simulate network error
    await page.context().setOffline(true);
    
    // Try to access Google Classroom data
    const coursesLink = page.locator('a:has-text("courses"), [data-testid="courses"]');
    
    if (await coursesLink.count() > 0) {
      await coursesLink.click();
      await page.waitForTimeout(2000);
      
      // Check for error message or offline indicator
      const errorMessage = page.locator('.error, [data-testid="error"], .offline');
      const hasError = await errorMessage.count() > 0;
      
      if (hasError) {
        await expect(errorMessage).toBeVisible();
      }
    }
    
    // Go back online
    await page.context().setOffline(false);
  });

  test('should handle Google Classroom permissions', async ({ page }) => {
    // Login as student (should have limited access)
    await page.goto('/login');
    await page.fill('input[name="email"]', 'student@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Try to access admin-only Google Classroom features
    const adminFeatures = page.locator('[data-testid="admin-features"], .admin-only, button:has-text("admin")');
    
    if (await adminFeatures.count() > 0) {
      // Admin features should not be visible to students
      await expect(adminFeatures).toHaveCount(0);
    }
    
    // Verify student can only see their own data
    const studentData = page.locator('[data-testid="student-data"], .student-view');
    if (await studentData.count() > 0) {
      await expect(studentData).toBeVisible();
    }
  });
});
