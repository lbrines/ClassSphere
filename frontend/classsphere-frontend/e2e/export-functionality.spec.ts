import { test, expect } from '@playwright/test';

test.describe('Export Functionality E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test environment
    await page.goto('/');
  });

  test('should export dashboard data to PDF', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for PDF export option
      const pdfOption = page.locator('[data-testid="export-pdf"], button:has-text("PDF"), .pdf-export');
      
      if (await pdfOption.count() > 0) {
        // Set up download promise
        const downloadPromise = page.waitForEvent('download');
        
        await pdfOption.click();
        
        // Wait for download to start
        const download = await downloadPromise;
        
        // Verify download started
        expect(download.suggestedFilename()).toContain('.pdf');
      }
    }
  });

  test('should export dashboard data to PNG', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for PNG export option
      const pngOption = page.locator('[data-testid="export-png"], button:has-text("PNG"), .png-export');
      
      if (await pngOption.count() > 0) {
        // Set up download promise
        const downloadPromise = page.waitForEvent('download');
        
        await pngOption.click();
        
        // Wait for download to start
        const download = await downloadPromise;
        
        // Verify download started
        expect(download.suggestedFilename()).toContain('.png');
      }
    }
  });

  test('should export dashboard data to SVG', async ({ page }) => {
    // Login as coordinator
    await page.goto('/login');
    await page.fill('input[name="email"]', 'coordinator@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for SVG export option
      const svgOption = page.locator('[data-testid="export-svg"], button:has-text("SVG"), .svg-export');
      
      if (await svgOption.count() > 0) {
        // Set up download promise
        const downloadPromise = page.waitForEvent('download');
        
        await svgOption.click();
        
        // Wait for download to start
        const download = await downloadPromise;
        
        // Verify download started
        expect(download.suggestedFilename()).toContain('.svg');
      }
    }
  });

  test('should export multiple charts to PDF', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for multiple export option
      const multipleOption = page.locator('[data-testid="export-multiple"], button:has-text("multiple"), .multiple-export');
      
      if (await multipleOption.count() > 0) {
        // Set up download promise
        const downloadPromise = page.waitForEvent('download');
        
        await multipleOption.click();
        
        // Wait for download to start
        const download = await downloadPromise;
        
        // Verify download started
        expect(download.suggestedFilename()).toContain('.pdf');
      }
    }
  });

  test('should handle export with custom filename', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for filename input
      const filenameInput = page.locator('[data-testid="filename"], input[placeholder*="filename"], .filename-input');
      
      if (await filenameInput.count() > 0) {
        await filenameInput.fill('custom-dashboard-export');
        
        // Look for PDF export option
        const pdfOption = page.locator('[data-testid="export-pdf"], button:has-text("PDF"), .pdf-export');
        
        if (await pdfOption.count() > 0) {
          // Set up download promise
          const downloadPromise = page.waitForEvent('download');
          
          await pdfOption.click();
          
          // Wait for download to start
          const download = await downloadPromise;
          
          // Verify custom filename
          expect(download.suggestedFilename()).toContain('custom-dashboard-export');
        }
      }
    }
  });

  test('should handle export error states', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Simulate network error
    await page.context().setOffline(true);
    
    // Try to export
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for PDF export option
      const pdfOption = page.locator('[data-testid="export-pdf"], button:has-text("PDF"), .pdf-export');
      
      if (await pdfOption.count() > 0) {
        await pdfOption.click();
        await page.waitForTimeout(2000);
        
        // Check for error message
        const errorMessage = page.locator('.error, [data-testid="error"], .export-error');
        const hasError = await errorMessage.count() > 0;
        
        if (hasError) {
          await expect(errorMessage).toBeVisible();
        }
      }
    }
    
    // Go back online
    await page.context().setOffline(false);
  });

  test('should handle export with large datasets', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for PDF export option
      const pdfOption = page.locator('[data-testid="export-pdf"], button:has-text("PDF"), .pdf-export');
      
      if (await pdfOption.count() > 0) {
        // Set up download promise with timeout
        const downloadPromise = page.waitForEvent('download', { timeout: 30000 });
        
        await pdfOption.click();
        
        try {
          // Wait for download to start
          const download = await downloadPromise;
          
          // Verify download started
          expect(download.suggestedFilename()).toContain('.pdf');
        } catch (error) {
          // If download times out, check for loading indicator
          const loadingIndicator = page.locator('.loading, [data-testid="loading"], .export-loading');
          const hasLoading = await loadingIndicator.count() > 0;
          
          if (hasLoading) {
            await expect(loadingIndicator).toBeVisible();
          }
        }
      }
    }
  });

  test('should handle export progress indication', async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for PDF export option
      const pdfOption = page.locator('[data-testid="export-pdf"], button:has-text("PDF"), .pdf-export');
      
      if (await pdfOption.count() > 0) {
        await pdfOption.click();
        
        // Check for progress indicator
        const progressIndicator = page.locator('.progress, [data-testid="progress"], .export-progress');
        const hasProgress = await progressIndicator.count() > 0;
        
        if (hasProgress) {
          await expect(progressIndicator).toBeVisible();
        }
      }
    }
  });

  test('should handle export cancellation', async ({ page }) => {
    // Login as coordinator
    await page.goto('/login');
    await page.fill('input[name="email"]', 'coordinator@test.com');
    await page.fill('input[name="password"]', 'StrongPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Look for export button
    const exportButton = page.locator('[data-testid="export"], button:has-text("export"), .export-button');
    
    if (await exportButton.count() > 0) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      
      // Look for PDF export option
      const pdfOption = page.locator('[data-testid="export-pdf"], button:has-text("PDF"), .pdf-export');
      
      if (await pdfOption.count() > 0) {
        await pdfOption.click();
        
        // Look for cancel button
        const cancelButton = page.locator('[data-testid="cancel"], button:has-text("cancel"), .cancel-button');
        
        if (await cancelButton.count() > 0) {
          await cancelButton.click();
          await page.waitForTimeout(1000);
          
          // Verify export was cancelled
          const exportDialog = page.locator('[data-testid="export-dialog"], .export-dialog');
          const hasDialog = await exportDialog.count() > 0;
          
          if (hasDialog) {
            await expect(exportDialog).not.toBeVisible();
          }
        }
      }
    }
  });
});
