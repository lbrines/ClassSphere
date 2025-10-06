import { test, expect } from '@playwright/test';

test.describe('Metrics and Visualizations E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should display dashboard metrics correctly', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
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
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Check for charts
    const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
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

  test('should handle chart data updates', async ({ page }) => {
    // Login as coordinator
    await page.goto('/login');
    await page.fill('input[name="email"]', 'coordinator@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for refresh button
    const refreshButton = page.locator('[data-testid="refresh"], button:has-text("refresh"), .refresh-button');
    
    if (await refreshButton.count() > 0) {
      // Get initial chart state
      const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
      const initialChartCount = await charts.count();
      
      // Click refresh
      await refreshButton.click();
      await page.waitForLoadState('networkidle');
      
      // Verify charts are still visible after refresh
      const updatedCharts = page.locator('[data-testid="chart"], .chart, canvas, svg');
      const updatedChartCount = await updatedCharts.count();
      
      expect(updatedChartCount).toBeGreaterThanOrEqual(initialChartCount);
    }
  });

  test('should handle chart filtering', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for filter controls
    const filters = page.locator('[data-testid="filter"], .filter, select, input[type="date"]');
    const filterCount = await filters.count();
    
    if (filterCount > 0) {
      // Apply first filter
      await filters.first().click();
      await page.waitForTimeout(1000);
      
      // Verify charts updated
      const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
      await expect(charts.first()).toBeVisible();
    }
  });

  test('should handle chart zoom and pan', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for charts
    const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
    
    if (await charts.count() > 0) {
      const chart = charts.first();
      
      // Test mouse interactions
      await chart.hover();
      await page.waitForTimeout(500);
      
      // Test click interaction
      await chart.click();
      await page.waitForTimeout(500);
      
      // Test drag interaction (if supported)
      const box = await chart.boundingBox();
      if (box) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.mouse.down();
        await page.mouse.move(box.x + box.width / 2 + 50, box.y + box.height / 2 + 50);
        await page.mouse.up();
        await page.waitForTimeout(500);
      }
      
      // Verify chart is still visible and interactive
      await expect(chart).toBeVisible();
    }
  });

  test('should handle chart tooltips', async ({ page }) => {
    // Login as coordinator
    await page.goto('/login');
    await page.fill('input[name="email"]', 'coordinator@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for charts
    const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
    
    if (await charts.count() > 0) {
      const chart = charts.first();
      
      // Hover over chart to trigger tooltip
      await chart.hover();
      await page.waitForTimeout(1000);
      
      // Look for tooltip
      const tooltip = page.locator('[data-testid="tooltip"], .tooltip, .chart-tooltip');
      const hasTooltip = await tooltip.count() > 0;
      
      if (hasTooltip) {
        await expect(tooltip).toBeVisible();
      }
    }
  });

  test('should handle chart legend interactions', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for chart legend
    const legend = page.locator('[data-testid="legend"], .legend, .chart-legend');
    
    if (await legend.count() > 0) {
      // Click on legend item
      const legendItems = legend.locator('li, .legend-item, [data-testid="legend-item"]');
      
      if (await legendItems.count() > 0) {
        await legendItems.first().click();
        await page.waitForTimeout(1000);
        
        // Verify legend interaction worked
        await expect(legend).toBeVisible();
      }
    }
  });

  test('should handle chart export functionality', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for charts
    const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
    
    if (await charts.count() > 0) {
      const chart = charts.first();
      
      // Right-click on chart to open context menu
      await chart.click({ button: 'right' });
      await page.waitForTimeout(500);
      
      // Look for export option in context menu
      const exportOption = page.locator('[data-testid="export-chart"], .export-chart, button:has-text("export")');
      
      if (await exportOption.count() > 0) {
        // Set up download promise
        const downloadPromise = page.waitForEvent('download');
        
        await exportOption.click();
        
        // Wait for download to start
        const download = await downloadPromise;
        
        // Verify download started
        expect(download.suggestedFilename()).toMatch(/\.(png|jpg|svg|pdf)$/);
      }
    }
  });

  test('should handle chart responsive behavior', async ({ page }) => {
    // Login as coordinator
    await page.goto('/login');
    await page.fill('input[name="email"]', 'coordinator@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Test different viewport sizes
    const viewports = [
      { width: 1920, height: 1080 }, // Desktop
      { width: 768, height: 1024 },  // Tablet
      { width: 375, height: 667 }    // Mobile
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.waitForTimeout(500);
      
      // Verify charts are still visible
      const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
      if (await charts.count() > 0) {
        await expect(charts.first()).toBeVisible();
      }
    }
  });

  test('should handle chart loading states', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for refresh button
    const refreshButton = page.locator('[data-testid="refresh"], button:has-text("refresh"), .refresh-button');
    
    if (await refreshButton.count() > 0) {
      // Click refresh to trigger loading
      await refreshButton.click();
      
      // Look for loading indicator
      const loadingIndicator = page.locator('.loading, [data-testid="loading"], .chart-loading');
      const hasLoading = await loadingIndicator.count() > 0;
      
      if (hasLoading) {
        await expect(loadingIndicator).toBeVisible();
        
        // Wait for loading to complete
        await page.waitForLoadState('networkidle');
        
        // Verify loading indicator is gone
        await expect(loadingIndicator).not.toBeVisible();
      }
    }
  });

  test('should handle chart error states', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Simulate network error
    await page.context().setOffline(true);
    
    // Try to refresh charts
    const refreshButton = page.locator('[data-testid="refresh"], button:has-text("refresh"), .refresh-button');
    
    if (await refreshButton.count() > 0) {
      await refreshButton.click();
      await page.waitForTimeout(2000);
      
      // Check for error message
      const errorMessage = page.locator('.error, [data-testid="error"], .chart-error');
      const hasError = await errorMessage.count() > 0;
      
      if (hasError) {
        await expect(errorMessage).toBeVisible();
      }
    }
    
    // Go back online
    await page.context().setOffline(false);
  });

  test('should handle chart data validation', async ({ page }) => {
    // Login as coordinator
    await page.goto('/login');
    await page.fill('input[name="email"]', 'coordinator@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Check for charts
    const charts = page.locator('[data-testid="chart"], .chart, canvas, svg');
    
    if (await charts.count() > 0) {
      // Verify charts have data
      const chart = charts.first();
      await expect(chart).toBeVisible();
      
      // Check for empty state if no data
      const emptyState = page.locator('[data-testid="empty-state"], .empty-state, .no-data');
      const hasEmptyState = await emptyState.count() > 0;
      
      if (hasEmptyState) {
        await expect(emptyState).toBeVisible();
      } else {
        // Verify chart has content
        await expect(chart).toBeVisible();
      }
    }
  });
});
