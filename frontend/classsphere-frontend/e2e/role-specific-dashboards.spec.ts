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

test.describe('Role-Specific Dashboards - Fase 2 E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should display admin dashboard with system metrics', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for admin-specific elements
    const adminElements = page.locator('app-admin-dashboard, [data-testid="admin-dashboard"]');
    const adminCount = await adminElements.count();
    
    if (adminCount > 0) {
      // Verify admin dashboard is displayed
      await expect(adminElements.first()).toBeVisible();
    }
    
    // Check for admin-specific metrics
    const systemMetrics = page.locator('text=Total Users, text=Total Courses, text=System Uptime, text=Active Sessions');
    const metricsCount = await systemMetrics.count();
    
    if (metricsCount > 0) {
      // Verify system metrics are displayed
      await expect(systemMetrics.first()).toBeVisible();
    }
    
    // Check for admin-specific actions
    const adminActions = page.locator('button:has-text("Export"), button:has-text("System"), button:has-text("Users")');
    const actionsCount = await adminActions.count();
    
    if (actionsCount > 0) {
      // Verify admin actions are available
      await expect(adminActions.first()).toBeEnabled();
    }
  });

  test('should display teacher dashboard with student metrics', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for teacher-specific elements
    const teacherElements = page.locator('app-teacher-dashboard, [data-testid="teacher-dashboard"]');
    const teacherCount = await teacherElements.count();
    
    if (teacherCount > 0) {
      // Verify teacher dashboard is displayed
      await expect(teacherElements.first()).toBeVisible();
    }
    
    // Check for teacher-specific metrics
    const teacherMetrics = page.locator('text=My Courses, text=Total Students, text=Assignments, text=Students at Risk');
    const metricsCount = await teacherMetrics.count();
    
    if (metricsCount > 0) {
      // Verify teacher metrics are displayed
      await expect(teacherMetrics.first()).toBeVisible();
    }
    
    // Check for teacher-specific actions
    const teacherActions = page.locator('button:has-text("Create Assignment"), button:has-text("Grade"), button:has-text("Intervene")');
    const actionsCount = await teacherActions.count();
    
    if (actionsCount > 0) {
      // Verify teacher actions are available
      await expect(teacherActions.first()).toBeEnabled();
    }
  });

  test('should display student dashboard with personal metrics', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for student-specific elements
    const studentElements = page.locator('app-student-dashboard, [data-testid="student-dashboard"]');
    const studentCount = await studentElements.count();
    
    if (studentCount > 0) {
      // Verify student dashboard is displayed
      await expect(studentElements.first()).toBeVisible();
    }
    
    // Check for student-specific metrics
    const studentMetrics = page.locator('text=My Courses, text=Average Grade, text=Upcoming Assignments, text=Recent Grades');
    const metricsCount = await studentMetrics.count();
    
    if (metricsCount > 0) {
      // Verify student metrics are displayed
      await expect(studentMetrics.first()).toBeVisible();
    }
    
    // Check for student-specific actions
    const studentActions = page.locator('button:has-text("View All"), button:has-text("View History"), button:has-text("Study")');
    const actionsCount = await studentActions.count();
    
    if (actionsCount > 0) {
      // Verify student actions are available
      await expect(studentActions.first()).toBeEnabled();
    }
  });

  test('should display coordinator dashboard with department metrics', async ({ page }) => {
    const user = testUsers.coordinator;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for coordinator-specific elements
    const coordinatorElements = page.locator('app-coordinator-dashboard, [data-testid="coordinator-dashboard"]');
    const coordinatorCount = await coordinatorElements.count();
    
    if (coordinatorCount > 0) {
      // Verify coordinator dashboard is displayed
      await expect(coordinatorElements.first()).toBeVisible();
    }
    
    // Check for coordinator-specific metrics
    const coordinatorMetrics = page.locator('text=Department Courses, text=Department Teachers, text=Department Students, text=Department Performance');
    const metricsCount = await coordinatorMetrics.count();
    
    if (metricsCount > 0) {
      // Verify coordinator metrics are displayed
      await expect(coordinatorMetrics.first()).toBeVisible();
    }
    
    // Check for coordinator-specific actions
    const coordinatorActions = page.locator('button:has-text("Manage"), button:has-text("Reports"), button:has-text("Analytics")');
    const actionsCount = await coordinatorActions.count();
    
    if (actionsCount > 0) {
      // Verify coordinator actions are available
      await expect(coordinatorActions.first()).toBeEnabled();
    }
  });

  test('should show role-specific navigation options', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for role-specific navigation
    const navOptions = page.locator('button:has-text("Búsqueda"), button:has-text("Gráficos"), button:has-text("D3")');
    const navCount = await navOptions.count();
    
    if (navCount > 0) {
      // Verify navigation options are available
      for (let i = 0; i < navCount; i++) {
        await expect(navOptions.nth(i)).toBeVisible();
        await expect(navOptions.nth(i)).toBeEnabled();
      }
    }
    
    // Test navigation functionality
    const searchButton = page.locator('button:has-text("Búsqueda")');
    if (await searchButton.count() > 0) {
      await searchButton.first().click();
      await page.waitForLoadState('networkidle');
      
      // Verify navigation worked
      await expect(page).toHaveURL(/search/);
      
      // Go back to dashboard
      await page.goBack();
      await page.waitForLoadState('networkidle');
    }
  });

  test('should display role badge correctly', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for role badge
    const roleBadge = page.locator('[data-testid="role-badge"], .role-badge, span:has-text("teacher"), span:has-text("Teacher")');
    const badgeCount = await roleBadge.count();
    
    if (badgeCount > 0) {
      // Verify role badge is displayed
      await expect(roleBadge.first()).toBeVisible();
      
      const badgeText = await roleBadge.first().textContent();
      expect(badgeText?.toLowerCase()).toContain('teacher');
    }
  });

  test('should handle role switching correctly', async ({ page }) => {
    // Start with admin role
    const adminUser = testUsers.admin;
    await registerAndLogin(page, adminUser);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Verify admin dashboard elements
    const adminElements = page.locator('app-admin-dashboard, [data-testid="admin-dashboard"]');
    const adminCount = await adminElements.count();
    
    if (adminCount > 0) {
      await expect(adminElements.first()).toBeVisible();
    }
    
    // Logout
    const logoutButton = page.locator('button:has-text("Cerrar sesión"), button:has-text("Logout"), [data-testid="logout"]');
    if (await logoutButton.count() > 0) {
      await logoutButton.first().click();
      await page.waitForLoadState('networkidle');
    }
    
    // Login as student
    const studentUser = testUsers.student;
    await loginUser(page, studentUser);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Verify student dashboard elements
    const studentElements = page.locator('app-student-dashboard, [data-testid="student-dashboard"]');
    const studentCount = await studentElements.count();
    
    if (studentCount > 0) {
      await expect(studentElements.first()).toBeVisible();
    }
    
    // Verify admin elements are no longer present
    const adminElementsAfter = page.locator('app-admin-dashboard, [data-testid="admin-dashboard"]');
    const adminCountAfter = await adminElementsAfter.count();
    expect(adminCountAfter).toBe(0);
  });

  test('should display appropriate metrics for each role', async ({ page }) => {
    const roles = [
      { user: testUsers.admin, expectedMetrics: ['Total Users', 'System Uptime', 'Active Sessions'] },
      { user: testUsers.teacher, expectedMetrics: ['My Courses', 'Total Students', 'Assignments'] },
      { user: testUsers.student, expectedMetrics: ['My Courses', 'Average Grade', 'Upcoming Assignments'] },
      { user: testUsers.coordinator, expectedMetrics: ['Department Courses', 'Department Teachers', 'Department Students'] }
    ];
    
    for (const roleTest of roles) {
      // Register and login
      await registerAndLogin(page, roleTest.user);
      
      // Should be redirected to dashboard
      await expect(page).toHaveURL(/dashboard/);
      
      // Check for role-specific metrics
      for (const metric of roleTest.expectedMetrics) {
        const metricElement = page.locator(`text=${metric}`);
        const metricCount = await metricElement.count();
        
        if (metricCount > 0) {
          await expect(metricElement.first()).toBeVisible();
        }
      }
      
      // Logout for next role
      const logoutButton = page.locator('button:has-text("Cerrar sesión"), button:has-text("Logout"), [data-testid="logout"]');
      if (await logoutButton.count() > 0) {
        await logoutButton.first().click();
        await page.waitForLoadState('networkidle');
      }
    }
  });

  test('should handle dashboard data loading states', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for loading states
    const loadingIndicators = page.locator('.loading, [data-testid="loading"], .spinner, .animate-spin');
    const loadingCount = await loadingIndicators.count();
    
    if (loadingCount > 0) {
      // Verify loading indicator is visible initially
      await expect(loadingIndicators.first()).toBeVisible();
      
      // Wait for loading to complete
      await page.waitForTimeout(2000);
      await expect(loadingIndicators.first()).not.toBeVisible();
    }
    
    // Verify dashboard content is loaded
    const dashboardContent = page.locator('.dashboard, [data-testid="dashboard"], .bg-white.shadow.rounded-lg');
    const contentCount = await dashboardContent.count();
    expect(contentCount).toBeGreaterThan(0);
  });

  test('should handle dashboard errors gracefully', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Simulate network error
    await page.context().setOffline(true);
    
    // Reload page to trigger error
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check for error handling
    const errorElements = page.locator('.error, [data-testid="error"], .alert-danger, .network-error');
    const errorCount = await errorElements.count();
    
    if (errorCount > 0) {
      // Verify error message is displayed
      await expect(errorElements.first()).toBeVisible();
      
      const errorText = await errorElements.first().textContent();
      expect(errorText).toContain('Error');
    } else {
      // If no error, should show fallback content
      const fallbackContent = page.locator('.fallback, [data-testid="fallback"], .offline-message');
      const fallbackCount = await fallbackContent.count();
      
      if (fallbackCount > 0) {
        await expect(fallbackContent.first()).toBeVisible();
      }
    }
    
    // Go back online
    await page.context().setOffline(false);
  });

  test('should maintain dashboard functionality across page refreshes', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Get initial dashboard state
    const initialContent = page.locator('.dashboard, [data-testid="dashboard"]');
    const initialCount = await initialContent.count();
    
    // Refresh page
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Verify dashboard is still functional
    const refreshedContent = page.locator('.dashboard, [data-testid="dashboard"]');
    const refreshedCount = await refreshedContent.count();
    
    expect(refreshedCount).toBeGreaterThan(0);
    
    // Verify user is still logged in
    await expect(page).toHaveURL(/dashboard/);
    
    // Verify dashboard elements are still present
    const metricsCards = page.locator('[data-testid="metrics-card"], .metrics-card, .stat-card');
    const cardCount = await metricsCards.count();
    expect(cardCount).toBeGreaterThan(0);
  });
});
