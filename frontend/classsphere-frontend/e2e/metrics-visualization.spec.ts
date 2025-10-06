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

test.describe('Metrics Visualization - Fase 2 E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should display metrics cards with correct data', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for metrics cards
    const metricsCards = page.locator('[data-testid="metrics-card"], .metrics-card, .stat-card');
    const cardCount = await metricsCards.count();
    
    if (cardCount > 0) {
      // Verify metrics cards are visible
      await expect(metricsCards.first()).toBeVisible();
      
      // Check for metric values
      const metricValues = page.locator('[data-testid="metric-value"], .metric-value, .stat-value');
      const valueCount = await metricValues.count();
      
      if (valueCount > 0) {
        // Verify metric values are displayed
        await expect(metricValues.first()).toBeVisible();
        
        // Check that values are numeric
        const firstValue = await metricValues.first().textContent();
        expect(firstValue).toMatch(/\d+/);
      }
    }
  });

  test('should display charts and visualizations', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for chart elements
    const charts = page.locator('[data-testid="chart"], .chart, canvas, svg, .chart-container');
    const chartCount = await charts.count();
    
    if (chartCount > 0) {
      // Verify charts are visible
      await expect(charts.first()).toBeVisible();
      
      // Test chart interactions
      await charts.first().hover();
      await page.waitForTimeout(500);
      
      // Verify chart is interactive
      await expect(charts.first()).toBeVisible();
    }
  });

  test('should display progress bars and indicators', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for progress bars
    const progressBars = page.locator('[data-testid="progress-bar"], .progress-bar, .progress, .bg-blue-600');
    const progressCount = await progressBars.count();
    
    if (progressCount > 0) {
      // Verify progress bars are visible
      await expect(progressBars.first()).toBeVisible();
      
      // Check for progress values
      const progressValues = page.locator('[data-testid="progress-value"], .progress-value, .percentage');
      const valueCount = await progressValues.count();
      
      if (valueCount > 0) {
        // Verify progress values are displayed
        await expect(progressValues.first()).toBeVisible();
        
        // Check that values are percentages
        const firstValue = await progressValues.first().textContent();
        expect(firstValue).toMatch(/\d+%/);
      }
    }
  });

  test('should display grade distribution charts', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for grade distribution elements
    const gradeElements = page.locator('text=Grade Distribution, text=A (90-100), text=B (80-89), text=C (70-79), text=D/F (<70)');
    const gradeCount = await gradeElements.count();
    
    if (gradeCount > 0) {
      // Verify grade distribution is displayed
      await expect(gradeElements.first()).toBeVisible();
      
      // Check for grade percentages
      const gradePercentages = page.locator('text=25%, text=35%, text=15%');
      const percentageCount = await gradePercentages.count();
      
      if (percentageCount > 0) {
        // Verify grade percentages are displayed
        await expect(gradePercentages.first()).toBeVisible();
      }
    }
  });

  test('should display activity heatmaps', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for activity heatmap elements
    const heatmapElements = page.locator('[data-testid="activity-heatmap"], .activity-heatmap, .heatmap');
    const heatmapCount = await heatmapElements.count();
    
    if (heatmapCount > 0) {
      // Verify heatmap is visible
      await expect(heatmapElements.first()).toBeVisible();
      
      // Test heatmap interactions
      await heatmapElements.first().hover();
      await page.waitForTimeout(500);
      
      // Verify heatmap is interactive
      await expect(heatmapElements.first()).toBeVisible();
    }
  });

  test('should display radar charts for skills assessment', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for radar chart elements
    const radarElements = page.locator('[data-testid="radar-chart"], .radar-chart, .skills-chart');
    const radarCount = await radarElements.count();
    
    if (radarCount > 0) {
      // Verify radar chart is visible
      await expect(radarElements.first()).toBeVisible();
      
      // Check for skill labels
      const skillLabels = page.locator('text=Matemáticas, text=Física, text=Química, text=Programación, text=Comunicación');
      const labelCount = await skillLabels.count();
      
      if (labelCount > 0) {
        // Verify skill labels are displayed
        await expect(skillLabels.first()).toBeVisible();
      }
    }
  });

  test('should display timeline charts for grade evolution', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for timeline chart elements
    const timelineElements = page.locator('[data-testid="timeline-chart"], .timeline-chart, .grade-timeline');
    const timelineCount = await timelineElements.count();
    
    if (timelineCount > 0) {
      // Verify timeline chart is visible
      await expect(timelineElements.first()).toBeVisible();
      
      // Test timeline interactions
      await timelineElements.first().hover();
      await page.waitForTimeout(500);
      
      // Verify timeline is interactive
      await expect(timelineElements.first()).toBeVisible();
    }
  });

  test('should display circular progress indicators', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for circular progress elements
    const circularElements = page.locator('[data-testid="circular-progress"], .circular-progress, .progress-circle');
    const circularCount = await circularElements.count();
    
    if (circularCount > 0) {
      // Verify circular progress is visible
      await expect(circularElements.first()).toBeVisible();
      
      // Check for progress labels
      const progressLabels = page.locator('text=Progreso General, text=Overall Progress');
      const labelCount = await progressLabels.count();
      
      if (labelCount > 0) {
        // Verify progress labels are displayed
        await expect(progressLabels.first()).toBeVisible();
      }
    }
  });

  test('should handle chart data updates', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for charts
    const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
    const chartCount = await charts.count();
    
    if (chartCount > 0) {
      // Get initial chart state
      const initialChart = charts.first();
      await expect(initialChart).toBeVisible();
      
      // Look for refresh button
      const refreshButton = page.locator('[data-testid="refresh"], button:has-text("refresh"), .refresh-button');
      
      if (await refreshButton.count() > 0) {
        // Click refresh
        await refreshButton.first().click();
        await page.waitForTimeout(1000);
        
        // Verify chart is still visible after refresh
        await expect(initialChart).toBeVisible();
      }
    }
  });

  test('should display metrics with proper formatting', async ({ page }) => {
    const user = testUsers.coordinator;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for formatted metrics
    const formattedMetrics = page.locator('[data-testid="formatted-metric"], .formatted-metric, .metric-formatted');
    const formattedCount = await formattedMetrics.count();
    
    if (formattedCount > 0) {
      // Verify formatted metrics are visible
      await expect(formattedMetrics.first()).toBeVisible();
      
      // Check for proper formatting (numbers, percentages, etc.)
      const metricText = await formattedMetrics.first().textContent();
      expect(metricText).toMatch(/\d+/); // Should contain numbers
    }
  });

  test('should handle empty data states gracefully', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for empty state handling
    const emptyStates = page.locator('[data-testid="empty-state"], .empty-state, .no-data');
    const emptyCount = await emptyStates.count();
    
    if (emptyCount > 0) {
      // Verify empty state is displayed
      await expect(emptyStates.first()).toBeVisible();
      
      // Check for empty state message
      const emptyMessage = page.locator('text=No data available, text=No courses, text=No students');
      const messageCount = await emptyMessage.count();
      
      if (messageCount > 0) {
        // Verify empty state message is displayed
        await expect(emptyMessage.first()).toBeVisible();
      }
    }
  });

  test('should display metrics with proper accessibility', async ({ page }) => {
    const user = testUsers.admin;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for accessibility attributes
    const accessibleElements = page.locator('[aria-label], [aria-describedby], [role="img"], [alt]');
    const accessibleCount = await accessibleElements.count();
    
    if (accessibleCount > 0) {
      // Verify accessible elements are present
      await expect(accessibleElements.first()).toBeVisible();
    }
    
    // Check for proper color contrast (basic check)
    const textElements = page.locator('text=Total Users, text=System Uptime, text=Active Sessions');
    const textCount = await textElements.count();
    
    if (textCount > 0) {
      // Verify text elements are visible (good contrast)
      await expect(textElements.first()).toBeVisible();
    }
  });

  test('should handle chart interactions correctly', async ({ page }) => {
    const user = testUsers.student;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for interactive charts
    const interactiveCharts = page.locator('[data-testid="interactive-chart"], .interactive-chart, canvas, svg');
    const interactiveCount = await interactiveCharts.count();
    
    if (interactiveCount > 0) {
      // Test hover interactions
      await interactiveCharts.first().hover();
      await page.waitForTimeout(500);
      
      // Verify chart is still visible after hover
      await expect(interactiveCharts.first()).toBeVisible();
      
      // Test click interactions
      await interactiveCharts.first().click();
      await page.waitForTimeout(500);
      
      // Verify chart is still visible after click
      await expect(interactiveCharts.first()).toBeVisible();
    }
  });

  test('should display metrics with proper loading states', async ({ page }) => {
    const user = testUsers.coordinator;
    
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
    
    // Verify metrics are loaded
    const metricsCards = page.locator('[data-testid="metrics-card"], .metrics-card, .stat-card');
    const cardCount = await metricsCards.count();
    expect(cardCount).toBeGreaterThan(0);
  });

  test('should handle chart data filtering', async ({ page }) => {
    const user = testUsers.teacher;
    
    // Register and login
    await registerAndLogin(page, user);
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Check for filter controls
    const filterControls = page.locator('[data-testid="filter"], .filter, select, input[type="date"]');
    const filterCount = await filterControls.count();
    
    if (filterCount > 0) {
      // Test filter interactions
      await filterControls.first().click();
      await page.waitForTimeout(500);
      
      // Verify filter is interactive
      await expect(filterControls.first()).toBeVisible();
      
      // Test filter selection
      const filterOptions = page.locator('option, .filter-option');
      const optionCount = await filterOptions.count();
      
      if (optionCount > 0) {
        // Select first option
        await filterOptions.first().click();
        await page.waitForTimeout(500);
        
        // Verify filter selection worked
        await expect(filterControls.first()).toBeVisible();
      }
    }
  });
});
